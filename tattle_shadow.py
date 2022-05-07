#!/usr/bin/env python3

"""This script pulls down yesterday's Shadowserver report"""

import sys
import re
from datetime import date, timedelta
import requests
import os
from shutil import copy2
import tattle_tale_cfg as cfg


def split_urls(full_link):
        """This function splits the URL and filename from the HTML string"""
        url1 = full_link.split(">")[1]
        url2 = url1.split("=")[1]
        url = url2.strip('"')
        file_name1 = full_link.split(">")[2]
        file_name = file_name1.split("<")[0]
        url_file ={}
        url_file[url] = file_name
        return (url_file)


def find_links(yesterday, yestermonth, importdata):
        """This function parses the HTML index for links to download."""
        f = importdata.splitlines()
        correct_month = False
        correct_day = False
        re_month = yestermonth
        re_day = yesterday
        matchme = "^  \<li\>{0}\<".format(re_month)
        match_day = "^    \<li\>{0}\<".format(re_day)
        match_next_month = "^  \<li\>[A-Z]"
        match_end_month = "^  \<\/ul\>\<\/li\>"
        match_end_day = "^    \<\/ul\>\<\/li\>"
        download_items = {}
        links = {}
        c = 0
        for i in f:
                if re.match(matchme, i) is not None:
                        correct_month = True
                if correct_month:
                        if re.match(match_end_day, i) is not None:
                                correct_day = False
                        if correct_day:
                                linkme = split_urls(i)
                                links[c] = linkme
                                c += 1
                        if re.match(match_day, i) is not None:
                                correct_day = True
                        if re.match(match_end_month, i) is not None:
                                correct_month = "false"
        return(links)

def find_yesterday():
        """This function finds yesterday's date"""
        today = date.today()
        yesterday = today - timedelta(days = 1)
        yesterday_day ="{0:%d}".format(yesterday)
        yesterday_month = "{0:%B}".format(yesterday)
        return yesterday_day, yesterday_month


def download_data(mysession, url, filename, path ):
        """This function downloads binary files and saves to the desired location"""
        save_as = path + filename
        response = mysession.get(url)
        with open(save_as, "w+b") as outfile:
                outfile.write(response.content)


def get_ip_addr(filename, service):
        with open(filename, "r") as infile:
                count = 0
                for line in infile:
                        fields = line.rstrip("\n").split(",")
                        #print(fields[1])
                        #ip_addr = fields[1]
                        if count > 0:
                                ip_addr = fields[1]
                                #print(ip_addr)
                                service_file = outdir + service + ".yml"
                                with open(service_file, "a") as opened_service_file:
                                        write_data(opened_service_file, ip_addr, service)
                        count += 1



def write_data(filename, ip_addr, service_name):
        filename.write(ip_addr + ': "' + service_name + '"\n')


def parse_data():
        file_list = os.scandir(filedir)
        for files in file_list:
                #print(files.name)
                if files.name.startswith("scan_"):
                        #print("Started with scan", files.name)
                        service_name = re.search("scan_(.+?)-charter_communications", files.name)
                else:
                        #print("Didn't start with scan", files.name)
                        service_name = re.search("^(.+?)-charter_communications", files.name)
                        #print("filedir", filedir + files.name)
                #print("service_name", service_name.group(1))
                #print("service_name", service_name)
                get_ip_addr(filedir + files.name, service_name.group(1))


def delete_files(directory):
        """ Delete all files in the provided directory"""
        for files in os.scandir(directory):
                delete_me = directory + files.name
                #print(delete_me)
                os.remove(delete_me)

def copy_files(source_dir, dest_dir):
        """Copy all files from one directory to another"""
        for files in os.scandir(source_dir):
                filename = source_dir + files.name
                copy2(filename, dest_dir)

#
#
download_dir = cfg.shadow_dir
# if this directory doesn't exist, create it
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
session = requests.Session()
credentials = {'user': cfg.shadow_user, 'password': cfg.shadow_pass, 'login':'Login'}
response = session.post(cfg.shadow_url, data=credentials)
print(f"Got response downloading ShadowServer report: {response.text} (status code {response.status_code})")
if response.status_code != 200:
        sys.exit(1)
yester_day_month = find_yesterday()
urls_files = find_links(yester_day_month[0], yester_day_month[1], response.text)


for key, value in urls_files.items():
        for nested_key, nested_value in value.items():
                fetch_url = nested_key
                save_as = nested_value
                download_data(session, fetch_url, save_as, download_dir)


filedir = cfg.shadow_dir
outdir = cfg.shadow_temp_dir
# if this directory doesn't exist, create it
if not os.path.exists(outdir):
    os.makedirs(outdir)
logstash_dir = cfg.logstash_dict_dir

# Clean out previous dictionary files
delete_files(outdir)
# Parse data and write new dictionary files
parse_data()
# Copy new dictionary files to permanent location
copy_files(outdir, logstash_dir)
