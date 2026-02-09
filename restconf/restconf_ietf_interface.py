import requests
import json
from dotenv import load_dotenv
import os
import sys
import urllib3
from pathlib import Path

def main():
    # désactive l'alerte généré par verify=False (ok pour lab)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # chemin vers le fichier contenant les variables d'envirronements
    cred_path = input(r"enter the path of your .env file (ex: path/to/file.env or C:\\path\to\file.env): ")
    cred_path_ft = Path(cred_path)

    if not cred_path_ft.exists():
        print("  --------------------------------------------------------------------------")
        print(" |  path doesn't exist, please restart the script and provide a valid path. |")
        print("  --------------------------------------------------------------------------")
        # (1) pour signaler qu'il y a eu une erreur au système
        sys.exit(1)

    # chargement des variables d'environnements
    load_dotenv(cred_path_ft)
    # Récupération des identifiants 
    username = os.getenv("username")
    password = os.getenv("password")    

    if not username or not password:
        print("Missing username or password in .env file")
        sys.exit(1)

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }   

    print("")
    print("--------------------------------------------------------------------------------------------------------------")
    print("This script can retrieve interfaces information and/or configure them.")
    print("--------------------------------------------------------------------------------------------------------------")
    print("")    
    device_ip = input("enter ip address of target device without netmask (ex: 10.10.10.10): ")  


    
    # variable dynamqiue (pour le payload et fct manage_int)
    def script_instructions():
      try:
        print("")
        print("--------------------------------------------------------------------------------------------------------------")
        print("There are two methods available !")
        print("get retrieves all interface information, patch adds an ipv4/netmask on the interface.")
        print("You can also create a Loopback address with patch.")
        print("--------------------------------------------------------------------------------------------------------------")
        print("")    
        print("available interface:")
        url_ietf_int_get = f"https://{device_ip}/restconf/data/ietf-interfaces:interfaces/interface"
        response = requests.get(url_ietf_int_get, auth=(username, password), headers=headers, verify=False)
        response.raise_for_status()
        all_inter = response.json()
        for inter in all_inter["ietf-interfaces:interface"]:
            if inter.get("ietf-ip:ipv4", {}).get("address", []):
              inter_name = inter['name'] 
              for address_mask in inter["ietf-ip:ipv4"]["address"]:
                  inter_ip = address_mask['ip']
                  inter_mask = address_mask['netmask']  
                  print(f"{inter_name}, ip: {inter_ip}, netmask: {inter_mask}")  
            else:
              print(f"{inter['name']}, no ip configured")
        print("-----------------------------------------------------------------------------------------------------------")
        print("")
        print("/!\ if you enter a non existant loopback address, it will be created.")
        int_name = input("enter interface name (ex: GigabitEthernet3, Loopback10): ")   

        if int_name.startswith("GigabitEthernet"):
            int_type = "iana-if-type:ethernetCsmacd"
        elif int_name.startswith("Loopback"):
            int_type = "iana-if-type:softwareLoopback"
        else:
            print("invalid interface name or the script may need to be adapted to the target device interfaces")
            sys.exit(1)
        method = input("enter get or patch: ")
        if method not in ("get", "patch"):
           print("invalid method, use get or patch")
           sys.exit(1)
        print("-----------------------------------------------------------------------------------------------------------")
        print("/!\ if you choose the get method, don't set anything and press enter to the two next steps")
        print("-----------------------------------------------------------------------------------------------------------")
        int_ip = input("enter ip address (ex: 10.10.10.10): ")
        int_mask = input("enter netmask (ex: 255.255.255.0): ")
        return int_name, int_type, int_ip, int_mask, method    
      except requests.HTTPError as e:
        print(e)    


    # récupère les variable entrée par l'utilisateur
    int_name, int_type, int_ip, int_mask, method = script_instructions()    

    # var URL
    url_ietf_int_get = f"https://{device_ip}/restconf/data/ietf-interfaces:interfaces/interface={int_name}"
    url_ietf_int_patch = f"https://{device_ip}/restconf/data/ietf-interfaces:interfaces/interface"  

    # Patch permet d'ajouter plusieurs adresses sur l'interface, un put peut écraser les adresses existantes
    payload_patch = {
        "ietf-interfaces:interface":[
        {
                    "name": int_name,
                    "description": "create via RESTCONF and ietf_interfaces",
                    "type": int_type,
                    "enabled": True,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": int_ip,
                                "netmask": int_mask
                            }
                        ]    
                    },
                    "ietf-ip:ipv6": {}
        }
      ] 
    }   




    def manage_int():
        if method == "patch":
            try:
                response = requests.patch(url_ietf_int_patch, auth=(username, password), headers=headers, data=json.dumps(payload_patch), verify=False)
                response.raise_for_status()
                print(response.status_code)
                print(f"interface {int_name} configured")
            except requests.HTTPError as e:
                print(e)          
        else:
            try:
                response = requests.get(url_ietf_int_get, auth=(username, password), headers=headers, verify=False)
                response.raise_for_status()
                print(response.text)
            except requests.HTTPError as e:
                print(e)        



    manage_int()

# evite que le script ce déclenche à l'import    
if __name__ == "__main__":
    main()