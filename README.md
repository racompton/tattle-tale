# Tattle Tale
A platform using the ELK stack to detect spoofed DDoS amplification request traffic with netflow to help perform traceback.  With Tattle Tale you can see which peers are sending you spoofed traffic and see which IPs in your network are receiving the most spoofed traffic.  You can also use it to determine if any hosts in your network are generating spoofed DDoS amplification request traffic.

Tattle Tale can scale horizontally to accomidate the largest networks in the world.  This is accomplished by adding additonal hosts that have Filebeat and Logstash.

Tattle Tale does not have very high requirements for disk storage or RAM (1TB/64GB should be fine) but Filebeat and Logstash are CPU hungry.  

## Installation instructions
Follow the install guide for installing Elasticsearch, Logstash, Kibana, and Filebeat.  Instructions can be found here: https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html

Install curator (also from Elastic).  Curator will remove entries from the elasticsearch database based on various rules (i.e. they are older than X months) Instructions can be found here: https://www.elastic.co/guide/en/elasticsearch/client/curator/current/installation.html

Clone this github repository `git clone https://github.com/racompton/tattle-tale/`

Copy the files from the `curator` directory and put them into `/etc/curator`

Copy the files from the `logstash` directory and put them into `/etc/logstash`

Copy the files from the `kibana` directory and put them into `/etc/kibana`

Edit the kibana.yml file and put in the `<hostname>`
  
Copy the files from the `elasticsearch` directory and put them into `/etc/elasticsearch`

Copy the files from the `filebeat` directory and put them into `/etc/filebeat`

Copy the file `delete_old_indices.sh` from the `cron.daily` directory to `/etc/cron.daily` and make the file executable (`chmod 755 /etc/cron.daily/delete_old_indices.sh`)

Create the `/opt/tattle-tale` directory `sudo mkdir /opt/tattle-tale`

Copy the `download-shadowserver-reports.py`, `call-api.py`, `.shadowserver.api`, `tattle_snmp_poll.py` and `tattle_tale_cfg.py` files to the `/opt/tattle-tale` directory and make `tattle_shadow.py` and `tattle_snmp_poll.py` executable (`chmod 755 <filename>`)

Edit the `.shadowserver.api` file to add in the credentials provided by Shadowserver.  If you don't yet receive Shadowserver reports, you can request credintials here: https://www.shadowserver.org/contact/

Rename the `netflow.yml.disabled` file to `netflow.yml` in `/etc/filebeat/modules.d`
Enable the filebeat module `sudo filebeat modules enable netflow` 

Edit the `tattle_tale_cfg.py` file and populate.  This field is the snmp community string for polling the routers to get their interface descriptions and SNMP index numbers.

`snmp_community = "<community string>"`


Create the file `/opt/tattle-tale/router_list.txt` and put in the IPs of routers that will be polled (one router per line). 


Restart the ELK stack daemons:
`sudo systemctl restart elasticsearch`
`sudo systemctl restart kibana`
`sudo systemctl restart logstash`
`sudo systemctl restart filebeat`

Make the ELK stack daemons start at boot:
`sudo systemctl enable elasticsearch`
`sudo systemctl enable kibana`
`sudo systemctl enable logstash`
`sudo systemctl enable filebeat`

Open Kibana and click the hamburger button to open up the left side menu.  Click "Stack Management" and then "Index patterns".  
Click the "+Create index pattern" button and put in "netflow*".  
Specify the primary time field as "@timestamp" from the drop down and press the "Create index pattern" button.

Optional step to create a dictionary file from the dissarm.net data (https://cablelabs.github.io/ddos-info-sharing/): uncomment out the `get-dissarm-ips.py` line in the `tattle_tale_shadow.sh` cron.daily script and then add in the API key and Org ID. Also rename the file `84-dis-abusers.conf.disabled` in `logstash/conf.d` to `84-dis-abusers.conf`.

FYI, you can use this command to get the interfaces, interface descriptions, and interface SNMP index numbers out of the Arbor Sightline `shell`: `sqlite3 /base/data/files/interface.db ".headers on" ".mode csv" "SELECT * FROM interfaces;" > /base/data/files/interfaces_classification.csv`  This can then be used to generate the `ifName.yml` file instead of using `tattle_snmp_poll.py`.
