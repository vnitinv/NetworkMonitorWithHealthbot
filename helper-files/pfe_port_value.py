#Jay Wilson, Wushu(Wilson) Ouyang

# using netmiko to show how flexible HB is.  Most JNPR people would used PYEZ
from netmiko import ConnectHandler
from junossecure.junos_secure import junos_decode

# define a routine to connect to a device and issue a command to JUNOS
def get_junos_command(device, command):
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command(command)
    net_connect.disconnect()
    return output

# Main routine for HB to run when called via a rule
def run():

    # get the device specifices from HB for the device that is being queried
    #     and create a python dictionary with the information that will be used
    #     for establishing a NETCONF session
    host = __pillar__["proxy"]["host"]
    user= __pillar__["proxy"]["username"]
    pwd = junos_decode(__pillar__["proxy"]["encoded_password"])
    device = {
       "device_type": "juniper_junos",
       "host": host,
       "username": user,
       "password": pwd,
       }
    # dictionary of what each BCM counter means. Can be used in trigger messages
    #     to explain what the traffic types the drop(s) are
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
    notdrops = ['TDBGC0', 'TDBGC2', 'TDBGC4']

    # commands that will be issued to a JUNOS device to retrieve specific VTP data
    command1 = 'request routing-engine execute command "/usr/sbin/cprod -A fpc0 -c \'show dcbc ifd all\' | awk \'NR > 3 {print $4}\' | xargs -I [] /usr/sbin/cprod -A fpc0 -c \'set dcbc bc \\"show c []\\"\' | awk \'/RDBGC0/ {print $0}; /TDBGC/ {print $0}\'"'
    command2 = 'request routing-engine execute command "/usr/sbin/cprod -A fpc0 -c \'show dcbc ifd all\'"'

    # issue "command1" to the specified JUNOS device
    output1 = get_junos_command(device,command1)
    #print(result)
    # NETCONF streams the data. split it into lines based on end of line character
    output1 = output1.split("\n")
    output1_list = []
    for line in output1:
        if line:
            line = line.split()
            # the counter is in the last column of output and it is a string
            value = line[3]
            # remove the + sign at the start of the string and any commas
            value = value[1:].replace(",", "")
            # convert the string to an integre to be stored by HB
            value = int(value)
            #print("value", value)
            # key is the counter name as listed in the meaning dictionary + a .<vty-port-index>
            #    we need to split out the counter name from the vty-port-index
            key = line[0]
            name = line[0].split(".")[0]
            #print("name", name)
            port = line[0].split(".")[1]
            #print("port", port)
            why = meaning.get(name)
            if notdrops.count(name) == 0 :
                output1_list.append({"tags": {"key": key}, "fields": {"name": name, "port":port, "value":value, "why":why}})

    # issue "command2" to the specified JUNOS device
    output2 = get_junos_command(device,command2)
    output2 = output2.split("\n")
    #  remove the first 3 lines because they are headers
    output2_new = output2[4:]

    ifd_port_list = []
    for item in output2_new:
        if item:
            item = item.split()
            ifd = item[0]
            port = item[4]
            ifd_port_list.append({"ifd":ifd, "port":port})

    # combine the output from the 2 commands based on the port number
    for item in output1_list:
        for ifd_port in ifd_port_list:
            if ifd_port["port"] == item["fields"]["port"]:
                item["fields"]["ifd"] = ifd_port["ifd"]

    #for item in output1_list: print(item)
    return output1_list
