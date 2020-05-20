# NetworkMonitorWithHealthbot
# [Automate Healthbot Configuration Using API](https://github.com/wouyang628/NetworkMonitorWithHealthbot/wiki/00-Automate-Healthbot-Configuration-Using-API)

To automate the Healthbot configuation deployment, we can utilize Healthbot API. For detailed information please refer [Healthbot API document](https://www.juniper.net/documentation/en_US/healthbot/information-products/pathway-pages/api-ref/healthbot-rca-api-2.1.0.html).

In this example, we add device, device groups, rules, playbooks, notifications ,etc.  
We can use python or ansible.
## 1. Using Python   
Using [config_healthbot.py](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/config_healthbot.py) to load Healthbot configuration in yaml format and post to Healthbot.

e.g.  
[devices.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/devices.yml)  
[device-groups.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/device-groups.yml)  
[network-groups.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/network-groups.yml)  
[notifications.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/notifications.yml)  
[rules.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/rules.yml)  
[playbooks.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/playbooks.yml)  

```
jcluser@ubuntu:~$ python3 config_healthbot.py
adding devices /n
succesfull
adding rules
succesfull
adding playbooks
succesfull
adding notifications
succesfull
adding device groups
succesfull
adding network groups
succesfull
commit heahlthbot configuration
commit succesfull
```

## 2. Using Ansible
Using Ansible's uri module to make api calls to Healthbot.
The playbook and role examples can be found here:  
[config_healthbot.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/config_healthbot.yml)  
[roles/config_healthbot/tasks/main.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/roles/config_healthbot/tasks/main.yml)  
[roles/config_healthbot/defaults/main.yml](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/roles/config_healthbot/defaults/main.yml)  

body content examples are here:  
[devices.json](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/devices.json)  
[device-groups.json](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/device-groups.json)  
[network-groups.json](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/network-groups.json)    
[notifications.json](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/notifications.json)  
[rules.json](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/rules.json)  
[playbooks.json](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/playbooks.json)  
```
[jcluser@centos hb_ansible]$ ansible-playbook config_hb1.yml
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [config hb] ****************************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [localhost]

TASK [config_healthbot : add devices to Healthbot] ******************************************************************************************************************
ok: [localhost]

TASK [config_healthbot : add rules to Healthbot] ********************************************************************************************************************
ok: [localhost]

TASK [config_healthbot : add playbooks to Healthbot] ****************************************************************************************************************
ok: [localhost]

TASK [config_healthbot : add notifications to Healthbot] ************************************************************************************************************
ok: [localhost]

TASK [config_healthbot : add device-groups to Healthbot] ************************************************************************************************************
ok: [localhost]

TASK [config_healthbot : add network-groups to Healthbot] ***********************************************************************************************************
ok: [localhost]

TASK [config_healthbot : commit Healthbot configuration] ************************************************************************************************************
ok: [localhost]

PLAY RECAP **********************************************************************************************************************************************************
localhost                  : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


[1. Y.1731 monitoring with iAgent](https://github.com/wouyang628/NetworkMonitorWithHealthbot/wiki/Y.1731-monitoring-with-iAgent)

[2. VPN Interface Monitoring Using Openconfig](https://github.com/wouyang628/NetworkMonitorWithHealthbot/wiki/VPN-Monitoring-Using-OpenConfig)

[3. collecting delay using OpenConfig and RPM](https://github.com/wouyang628/NetworkMonitorWithHealthbot/wiki/collecting-delay-using-openconfig)

[4. Syslog as Ingest](https://github.com/wouyang628/NetworkMonitorWithHealthbot/wiki/syslog-as-ingest)

[5. SNMP as Ingest](https://github.com/wouyang628/NetworkMonitorWithHealthbot/wiki/SNMP-as-Ingest)


 interface traffic monitoring with OpenConfig

 collecting LSP statis with native sensor JTI





for using iagent, please make sure the related rpc yml files are under /var/local/healthbot/input
