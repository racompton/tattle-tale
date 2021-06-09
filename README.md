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
Copy the `tattle_shadow.py`, `tattle_snmp_poll.py` and `tattle_tale_cfg.py` files to the `/usr/bin/` directory and make `tattle_shadow.py` and `tattle_snmp_poll.py` executable (`chmod 755 <filename>`)

Rename the `netflow.yml.disabled` file to `netflow.yml` in `/etc/filebeat/modules.d`
Enable the filebeat module `sudo filebeat modules enable netflow` 

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




