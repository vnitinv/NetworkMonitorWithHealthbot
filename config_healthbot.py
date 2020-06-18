import os
import json
import yaml
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Healthbot(object):
    def __init__(self):
        self.server_ip = "66.129.235.12:49022"
        self.base_url = "https://" + self.server_ip + "/api/v1/"
        self.headers = {"Accept":"application/json", "Content-Type":"application/json"}
        self.username = "jcluser"
        self.passwd = "Juniper!1"
        self.devices_file = "devices.yml"
        self.rule_directory = "rules/"
        self.playbook_directory = "playbooks/"
        self.helper_file_directory = "helper-files/"
        self.notifications_file = "notifications.yml"
        self.device_groups_file = "device-groups.yml"
        self.network_groups_file = "network-groups.yml"

    #load the yaml file and convert to json payload
    def read_payload(self, file_to_read):
        f = open(file_to_read, "r")
        txt = f.read()
        f.close()
        #payload = json.dumps(txt)
        return(txt)

    def post_to_healthbot(self, url, payload):
        #payload = self.read_payload(yml_file)
        r = requests.post(url, auth=HTTPBasicAuth(self.username, self.passwd), headers=self.headers, verify=False, data=payload)
        if r.status_code == 200:
          print("succesfull")
        else:
          print("failed")
          print(r.content)
        return(r)

    def commit_healthbot(self):
        r = requests.post(self.base_url + "/configuration", auth=HTTPBasicAuth(self.username, self.passwd), headers=self.headers, verify=False)
        if r.status_code == 200:
          print("commit succesfull")
        else:
          print("failed")
          print(r.content)
        return(r)

    def add_a_rule(self, topic_name, payload):
        add_a_rule_url = self.base_url + "topic/" + topic_name
        r = self.post_to_healthbot(add_a_rule_url, payload)
        return(r)

    def add_rules(self):
        for filename in os.listdir(self.rule_directory):
            #print("filename: " + filename)
            file_to_read = self.rule_directory + filename
            payload_rule = self.read_payload(file_to_read)
            payload_dic = json.loads(payload_rule)
            topic_name = payload_dic["topic-name"]
            rule_name = payload_dic["rule"][0]["rule-name"]
            print("adding a rule: " + topic_name + " " + rule_name)
            r = self.add_a_rule(topic_name, payload_rule)

    def add_a_playbook(self, payload):
        add_a_playbook_url = self.base_url + "playbooks/"
        r = self.post_to_healthbot(add_a_playbook_url, payload)
        return(r)

    def add_playbooks(self):
        for filename in os.listdir(self.playbook_directory):
            #print("filename: " + filename)
            file_to_read = self.playbook_directory + filename
            payload_playbook = self.read_payload(file_to_read)
            payload_dic = json.loads(payload_playbook)
            playbook_name = payload_dic["playbook"][0]["playbook-name"]
            print("adding playbook: " + playbook_name)
            r = self.add_a_playbook(payload_playbook)        

    def upload_a_helper_file(self, filename, payload_helper):
        headers = {"Accept":"application/json"}
        upload_helper_file_url = self.base_url + "/files/helper-files/" + filename
        r = requests.post(upload_helper_file_url, auth=HTTPBasicAuth(self.username, self.passwd), headers=headers, verify=False, files=payload_helper)
        if r.status_code == 200:
            print("succesfull")
        else:
            print("failed")
            print(r.content)
        return(r)

    def upload_helper_files(self):
         for filename in os.listdir(self.helper_file_directory):
            #print("filename: " + filename)
            file_to_read = self.helper_file_directory + filename
            payload_helper = {"up_file": self.read_payload(file_to_read)}
            print("adding helper file: " + filename)
            r = self.upload_a_helper_file(filename, payload_helper)        

if __name__ == '__main__':
    hb= Healthbot()
    #hb.add_rules()
    #hb.add_playbooks()
    hb.upload_helper_files()
    #hb.commit_healthbot()
'''
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
r = post_to_healthbot(add_notifications_url, notifications_file)

"""
#### add device groups ####
add_device_groups_url = base_url+ "device-groups"
print("adding device groups")
r = post_to_healthbot(add_device_groups_url, device_groups_file)
"""

"""
#### add network groups ####
add_network_groups_url = base_url+ "network-groups"
print("adding network groups")
r = post_to_healthbot(add_network_groups_url, network_groups_file)
"""

#### commit healthbot configuration ####
print("commit heahlthbot configuration")
commit_healthbot()
'''