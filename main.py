import csv
import time


def set_netmask(mask):

    masks_list = []

    mask_mapping = {

        "/18": "255.255.192.0",
        "/19": "255.255.224.0",
        "/20": "255.255.240.0",
        "/21": "255.255.248.0",
        "/22": "255.255.252.0",
        "/23": "255.255.254.0",
        "/24": "255.255.255.0",
        "/25": "255.255.255.128",
        "/26": "255.255.255.192",
        "/27": "255.255.255.224",
        "/28": "255.255.255.240",
        "/29": "255.255.255.248",
        "/30": "255.255.255.252",

    }

    for item in mask:
        item = item.strip()
        for k, v in mask_mapping.items():
            if item == k:
                masks_list.append(v)

    return masks_list


def get_vlan_name_no(list1):

    farm_name = []
    vlan_no = []

    for element in list1:
        element = element.split("-")
        farm_name.append(element[0])
        vlan_no.append(element[1])

    return farm_name, vlan_no


def config(epg_list, farm_list, vlan_list, ip1_list, ip2_list, netmask_list, choice):

    print("\n\n[+] Config for ROUTER 1\n-------------------------------------\n")

    for epg, farm, vlan, ip1, netmask in zip(epg_list, farm_list, vlan_list, ip1_list, netmask_list):

        print("interface GigabitEthernet0/0." + str(epg))
        print("description to " + farm + "_V" + vlan + "_EPG_" + str(epg) + " (2105-1/47)")
        print("encapsulation dot1Q " + str(epg))

        if choice == "dev":
            print("vrf forwarding dev")

        print("ip address " + str(ip1) + " " + netmask)
        print("ip helper-address xxxxxxxxx")
        print("no ip proxy-arp")
        print("no cdp enable\n!")

        epg = int(epg)
        epg += 1

    print("\n\n[+] Config for ROUTER 2\n-------------------------------------\n")

    for epg, farm, vlan, ip2, netmask in zip(epg_list, farm_list, vlan_list, ip2_list, netmask_list):

        print("interface GigabitEthernet0/0." + str(epg))
        print("description to " + farm + "_V" + vlan + "_EPG_" + str(epg) + " (2205-1/47)")
        print("encapsulation dot1Q " + str(epg))

        if choice == "dev":
            print("vrf forwarding dev")

        print("ip address " + str(ip2) + " " + netmask)
        print("ip helper-address xxxxxx")
        print("no ip proxy-arp")
        print("no cdp enable\n!")
        epg = int(epg)
        epg += 1


if __name__ == "__main__":

    while True:

        choice1 = input("\n[+] Hello, would you like to configure prod or dev? (type prod/dev): ")

        choice_list = ["prod", "dev"]

        if choice1 not in choice_list:
            print("\n[-] Please enter either prod or dev!")

        else:
            break

    print("\n[+] Generating config, please wait...")
    time.sleep(2)

    choice = str(choice1)
    choice += ".csv"

    with open("data.csv", 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")

        epg_no = []
        containers = []
        ip1 = []
        ip2 = []
        netmasks = []

        for row in reader:

            if row[0] == "VLAN-ID":
                pass

            else:
                epg_no.append(row[0].strip())
                containers.append(row[1].strip())
                ip1.append(row[2].strip())
                ip2.append(row[3].strip())
                netmasks.append(row[4].strip())

        farm, vlan = get_vlan_name_no(containers)
        masks = set_netmask(netmasks)
        config(epg_no, farm, vlan, ip1, ip2, masks, choice1)

        print("\n\n------------------\n\n[+] Configured a total of {} interfaces.".format(len(farm)))

        input("\n[+] Press ENTER to exit.")

