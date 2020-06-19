# NetworkMonitorWithHealthbot
Automate Healthbot Configuration Using API

To automate the Healthbot configuation deployment, we can utilize Healthbot API. For detailed information please refer [Healthbot API document](https://www.juniper.net/documentation/en_US/healthbot/information-products/pathway-pages/api-ref/healthbot-rca-api-2.1.0.html).

In this example, we add device, device groups, rules, playbooks, notifications ,etc.  
We can use python or ansible.

## 1. Using Python   
Using [config_healthbot.py](https://github.com/wouyang628/NetworkMonitorWithHealthbot/blob/master/config_healthbot.py) to load Healthbot configuration and post to Healthbot.

Please change the settings in settings.json according to your enviroment.

e.g.  
[devices.yml](devices.yml)  
[device-groups.yml](device-groups.yml)  
[network-groups.yml](network-groups.yml)  
[notifications.yml](notifications.yml)  
[rules.yml](rules.yml)  
[playbooks.yml](playbooks.yml)  

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
[config_healthbot.yml](config_healthbot.yml)  
[roles/config_healthbot/tasks/main.yml](roles/config_healthbot/tasks/main.yml)  
[roles/config_healthbot/defaults/main.yml](roles/config_healthbot/defaults/main.yml)  

body content examples are here:  
[devices.json](devices.json)  
[device-groups.json](device-groups.json)  
[network-groups.json](network-groups.json)    
[notifications.json](notifications.json)  
[rules.json](rules.json)  
[playbooks.json](playbooks.json)  

Please update the server ip and user credential in  
[roles/config_healthbot/defaults/main.yml](roles/config_healthbot/defaults/main.yml)
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







