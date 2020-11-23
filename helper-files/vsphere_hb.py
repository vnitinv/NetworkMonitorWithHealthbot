#specify vsphere IP (not esxi)

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

import atexit
import ssl
from junossecure.junos_secure import junos_decode

def GetDatacenterVM(content):
    datacenter_view = content.viewManager.CreateContainerView(content.rootFolder, 
                                                                     [vim.Datacenter], 
                                                                     True)
    datacenters = datacenter_view.view

    vm_list = []

    for datacenter in datacenters:
        print("datacenter", datacenter)
        if hasattr(datacenter.hostFolder, 'childEntity'):
            clusters = datacenter.hostFolder.childEntity
            print(datacenter.hostFolder.childEntity)
            for cluster in clusters:
                print("cluster", cluster.name)
                #print("group name", group.name)
                if hasattr(cluster, 'childEntity'):
                    hosts = cluster.childEntity
                    #print("hosts", hosts)
                    for host in hosts:
                        #print("host ", host)
                        hosts2 = host.host
                        #print("host.host", host.host)
                        for host2 in hosts2:
                            print("host2",host2, host2.name)
                            #print("vm", host2.vm)
                            vm2 = host2.vm
                            for vm in vm2:
                                print("vm name", vm.name)
                                ip = "None"
                                mac = "None"
                                if vm.summary.guest != None:
                                    ip = vm.summary.guest.ipAddress
                                    #print("ip", ip)
                                if vm.config != None:
                                    #print("########vm config name######")
                                    #print(vm.config)
                                    #print("########end of vm config######")
                                    for device in vm.config.hardware.device:
                                        #print("########device######")
                                        #print(type(device))
                                        #print(device)
                                        #print("########end of device######")
                                        if hasattr(device, 'macAddress'):
                                            mac = device.macAddress
                                            #print("mac", mac)                
                                vm_list.append({'tags': {"name": vm.name}, "fields": {"ip": ip, "mac": mac, "host":host2.name, "cluster":cluster.name, "datacenter":datacenter.name}})
        
    #for vm in vm_list:
    #  print(vm)
    return vm_list


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
    
    vm_host_cluster_datacenter = GetDatacenterVM(content)
    return vm_host_cluster_datacenter
