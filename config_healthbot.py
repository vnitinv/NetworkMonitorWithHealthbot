import os
import json
import yaml
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


server_ip = "100.123.0.19:8080"
base_url = "https://" + server_ip + "//api/v1/"
headers = {"Accept":"application/json", "Content-Type":"application/json"}
username = "jcluser"
passwd = "Juniper!1"
devices_file = "devices.yml"
rules_file = "rules.yml"
playbooks_file = "playbooks.yml"
notifications_file = "notifications.yml"
device_groups_file = "device-groups.yml"
network_groups_file = "network-groups.yml"


#load the yaml file and convert to json payload
def read_payload(file_to_read):
    f = open(file_to_read, "r")
    txt = f.read()
    f.close()
    payload = json.dumps(yaml.load(txt))
    return(payload)

def post_to_healthbot(url, yml_file):
    payload = read_payload(yml_file)
    r = requests.post(url, auth=HTTPBasicAuth(username, passwd), headers=headers, verify=False, data=payload)
    if r.status_code == "200":
      print("succesfull")
    else:
      print("failed")
      print(r.content)
    return(r)

def commit_healthbot():
    r = requests.post(base_url + "/configuration", auth=HTTPBasicAuth(username, passwd), headers=headers, verify=False)
    if r.status_code == "200":
      print("commit succesfull")
    else:
      print("failed")
      print(r.content)
    return(r)

#### add devices ####
add_devices_url = base_url+ "devices"
print("adding devices")
r = post_to_healthbot(add_devices_url, devices_file)

#### add rules ####
add_rules_url = base_url+ "topics"
print("adding rules")
r = post_to_healthbot(add_rules_url, rules_file)

#### add playbooks ####
add_playbooks_url = base_url+ "playbooks"
print("adding playbooks")
r = post_to_healthbot(add_playbooks_url, playbooks_file)

#### add notifications ####
add_notifications_url = base_url+ "notifications"
print("adding notifications")
r = post_to_healthbot(add_playbooks_url, notifications_file)

#### add device groups ####
add_device_groups_url = base_url+ "device-groups"
print("adding device groups")
r = post_to_healthbot(add_device_groups_url, device_groups_file)

#### add network groups ####
add_network_groups_url = base_url+ "network-groups"
print("adding network groups")
r = post_to_healthbot(add_network_groups_url, network_groups_file)

#### commit healthbot configuration ####
print("commit heahlthbot configuration")
commit_healthbot()
