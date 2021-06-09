#!/usr/bin/env python3
from snimpy.manager import Manager as M
from snimpy.manager import load
from snimpy.snmp import SNMPException
import re
import tattle_tale_cfg as cfg

community = cfg.snmp_community

def poll_snmp(device_ip):
        load("IF-MIB")
        m = M(device_ip, community, 2)
        #m = M(device_ip, cfg.community, 2)
        #
        name = {}
        try:
                for index, value in m.ifAlias.iteritems():
                        if value:
                                name.update({str(index):{"IP":device_ip, "desc": str(value)}})
                                #print(name)
        except SNMPException:
                pass
                #print("Unable to poll", device_ip.rstrip("\n"))
        except UnicodeDecodeError:
                pass
                #print("Unable to parse", device_ip.rstrip("\n"), index, value)
        return(name)


def parse_ifAlias(input_string):
        try:
                extracted = re.search(cfg.if_regex, input_string)
                #test = extracted.group(1)
                #return(test)
                return(extracted.group(1))
        except:
                pass



def doit():
        with open(cfg.device_list, "r") as in_file:
                combined = {}
                for line in in_file:
                        #print(line)
                        combined.update(poll_snmp(line))
        #
        with open(cfg.logstash_dict_dir+"/ifName.yml", "w") as save_file:
                for index, values in combined.items():
                        peer_name = parse_ifAlias(values["desc"])
                        #peer_name = values["desc"]
                        if peer_name:
                                #out_string = '"' + values["IP"].rstrip("\n") + '::ifName.' + index + '": "' + values["desc"] + '"'
                                out_string = '"' + values["IP"].rstrip("\n") + '::ifName.' + index + '": "' + peer_name + '"'
                                #print(out_string)
                                save_file.write(out_string + "\n")

doit()
