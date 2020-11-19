#Jay Wilson, Wushu(Wilson) Ouyang

from netmiko import ConnectHandler
from junossecure.junos_secure import junos_decode

def get_junos_command(device, command):
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command(command)
    net_connect.disconnect()
    return output


def run():

    host = __pillar__["proxy"]["host"]
    user= __pillar__["proxy"]["username"]
    pwd = junos_decode(__pillar__["proxy"]["encoded_password"])
    device = {
       "device_type": "juniper_junos",
       "host": host,
       "username": user,
       "password": pwd,
       }
    meaning = {
        'RDBGC0': '(All Received Drop)',
        'RDBGC1': '(Filter Block Drop)',
        'RDBGC2': '(Multicast Drop)',
        'RDBGC3': '(VLAN Drop)',
        'RDBGC4': '(Policy Discard Drop)',
        'RDBGC5': '(Parity Error Drop)',
        'RDBGC6': '(VLAN Field Processor Drop)',
        'RDBGC7': '(L2/L3 Lookup DST_DISCARD Drop)',
        'RDBGC8': '(11 other error Drops)',
        'TDBGC1': '(IPv6 L3 and IPMC Aged and Drop)',
        'TDBGC3': '(All Transmit Drop)',
        'TDBGC5': '(IPv4 L3 and IPMC Aged and Drop)',
        'TDBGC6': '(L2 Multicast Drop)',
        'TDBGC7': '(Aged Drop)',
        'TDBGC8': '(STP not in FWD state Drop)',
        'TDBGC9': '(VXLT Translate Drop)',
        'TDBGC10': '(Invalid VLAN Drop)',
        'TDBGC11': '(6 other error Drops)',
    }
    command1 = 'request routing-engine execute command "/usr/sbin/cprod -A fpc0 -c \'show dcbc ifd all\' | awk \'NR > 3 {print $4}\' | xargs -I [] /usr/sbin/cprod -A fpc0 -c \'set dcbc bc \\"show c []\\"\' | awk \'/RDBGC0/ {print $0}; /TDBGC/ {print $0}\'"'
    command2 = 'request routing-engine execute command "/usr/sbin/cprod -A fpc0 -c \'show dcbc ifd all\'"'


    output1 = get_junos_command(device,command1)
    #print(result)
    output1 = output1.split("\n")
    output1_list = []
    for line in output1:
        if line:
            line = line.split()
            value = line[3]
            value = value[1:].replace(",", "")
            value = int(value)
            #print("value", value)
            key = line[0]
            name = line[0].split(".")[0]
            #print("name", name)
            port = line[0].split(".")[1]
            #print("port", port)
            why = meaning.get(name)
            output1_list.append({"tags": {"key": key}, "fields": {"name": name, "port":port, "value":value, "why":why}})


    output2 = get_junos_command(device,command2)
    output2 = output2.split("\n")
    #remove the first 3 header lines
    output2_new = output2[4:]

    ifd_port_list = []
    for item in output2_new:
        if item:
            item = item.split()
            ifd = item[0]
            port = item[4]
            ifd_port_list.append({"ifd":ifd, "port":port})


    for item in output1_list:
        for ifd_port in ifd_port_list:
            if ifd_port["port"] == item["fields"]["port"]:
                item["fields"]["ifd"] = ifd_port["ifd"]

    #for item in output1_list: print(item)
    return output1_list
