from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import argparse
import atexit
import getpass
import ssl
from junossecure.junos_secure import junos_decode

def GetVMs(content):

    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    obj = [vm for vm in vm_view.view]
    vm_view.Destroy()
    return obj


def run():

   host = __pillar__["proxy"]["vcenter"]
   user= __pillar__["proxy"]["username"]
   pwd = junos_decode(__pillar__["proxy"]["encoded_password"])
   port = __pillar__["proxy"]["port"]

   context = None
   if hasattr(ssl, '_create_unverified_context'):
      context = ssl._create_unverified_context()
   #si = __salt__["vsphere.get_service_instance_via_proxy"]()
   si = SmartConnect(host=host,
                     user=user,
                     pwd=pwd,
                     port=port,
                     sslContext=context)
   if not si:
       print("Could not connect to the specified host using specified "
             "username and password")
       return -1

   atexit.register(Disconnect, si)

   content = si.RetrieveContent()
   vms = GetVMs(content)
   vm_list = []
   for vm in vms:
       print(" ")
       #print(vm.summary)
       #print("####end of vm######")
       if vm.summary.guest != None:
         ip = vm.summary.guest.ipAddress
         name = vm.summary.config.name
       #print("Name       : ", name)
       #print("IP         : ", ip)
       if vm.config != None:
         #print("########vm config name######")
         #print(vm.config)
         for device in vm.config.hardware.device:
           #print("########device######")
           #print(type(device))
           #print(device)
           if hasattr(device, 'macAddress'):
             mac = device.macAddress
             #print("MAC        : ", mac)
       vm_list.append({'tags': {"name": name}, "fields": {"ip": ip, "mac": mac}})
   return vm_list
