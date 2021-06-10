# tattle-tale
A platform using the ELK stack to detect spoofed UDP DDoS amplification request traffic with netflow 

## Installation instructions
Follow the install guide for installing Elasticsearch, Logstash, Kibana, and Filebeat.  Instructions can be found here: https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html

Install curator (also from Elastic).  Instructions can be found here: https://www.elastic.co/guide/en/elasticsearch/client/curator/current/installation.html

Clone this github repository `git clone https://github.com/racompton/tattle-tale/`

Copy the files from the `curator` directory and put them into `/etc/curator`

Copy the files from the `logstash` directory and put them into `/etc/logstash`

Copy the files from the `filebeat` directory and put them into `/etc/filebeat`

Copy the file `delete_old_indicies.sh` from the `cron.daily` directory to `/etc/cron.daily` and make the file executable (`chmod 755 /etc/cron.daily/delete_old_indicies.sh`)

Create the `/opt/tattle_tale` directory `sudo mkdir /opt/tattle_tale`

Copy the `tattle_shadow.py`, `tattle_snmp_poll.py` and `tattle_tale_cfg.py` files to the `/opt/tattle_tale` directory and make `tattle_shadow.py` and `tattle_snmp_poll.py` executable (`chmod 755 <filename>`)

Rename the `netflow.yml.disabled` file to `netflow.yml` in `/etc/filebeat/modules.d`
Enable the filebeat module `sudo filebeat modules enable netflow` 

Edit the `tattle_tale_cfg.py` file and populate these fields:

**These fields will be populated with the email address/password that Shadowserver has assigned to you.  If you don't yet receive Shadowserver reports, you can request them here: https://www.shadowserver.org/contact/

`shadow_user = "<username>"`

`shadow_pass = "<password>"`

**This field is the snmp community string for polling the routers for their interface descriptions

`snmp_community = "<community string>"`


Create the file `/opt/tattle_tale/router_list.txt` and put in the IPs of routers that will be polled (one router per line). 


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




