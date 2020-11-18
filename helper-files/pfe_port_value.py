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
            value = value[1:]
            value = int(value)
            #print("value", value)
            key = line[0]       
            name = line[0].split(".")[0]
            #print("name", name)
            port = line[0].split(".")[1]
            #print("port", port)
            output1_list.append({"tags": {"key": key}, "fields": {"name": name, "port":port, "value":value}})


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