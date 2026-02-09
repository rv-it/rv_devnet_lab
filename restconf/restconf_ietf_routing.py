import requests
import json
from dotenv import load_dotenv
import os
import urllib3
from pathlib import Path
import sys


def main():
    # désactive l'alerte généré par verify=False (ok pour lab)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # chemin vers le fichier contenant les variables d'envirronements
    cred_path = input(r"enter the path of your .env file (ex: path/to/file.env or C:\\path\to\file.env): ")
    cred_path_ft = Path(cred_path)

    if not cred_path_ft.exists():
        print("  ---------------------------------------------------------------------------")
        print(" |  path doesn't exist, please restart the script and provide a valid path.  |")
        print("  ---------------------------------------------------------------------------")
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
        "Content-type": "application/yang-data+json"
    }   

    # variable dynamique pour les payload
    print("")
    print("------------------------------------------------------------------------------------")
    print("This script adds a static route to a VRF instance")
    print("/!\ if the VRF instance doesn't exist, it will be created")
    print("------------------------------------------------------------------------------------")
    print("")
    device_ip = input("enter ip address of target device without netmask (ex: 10.10.10.10): ")
    print("------------------------------------------------------------------------------------")
    print("VRF instances info:")
    print("------------------------------------------------------------------------------------")    
    url = f"https://{device_ip}/restconf/data/ietf-routing:routing"
    try:
        response = requests.get(url, auth=(username, password), headers=headers, verify=False)
        data=response.json()
        data_ft = json.dumps(data, indent= 4)
        print(data_ft)
        print("------------------------------------------------------------------------------------")
        print("")
        print("------------------------------------------------------------------------------------")
        i = 1
        for instance in data["ietf-routing:routing"]["routing-instance"]:
            print(f"{len(data['ietf-routing:routing']['routing-instance'])} VRF instance/s available/s")
            print(f"VRF instance {i} - name: {instance['name']}")
            i += 1
            print("------------------------------------------------------------------------------------")
            print("")
    except requests.HTTPError as e:
        print(e)
    
    inst_name = input("VRF instance name (no spaces, accents or special characters): ")
    dest_net = input("Destination network (IP/CIDR, ex: 172.31.4.0/24): ")
    next_hop = input("next hop address without mask (ex: 10.10.10.1): ")    

    # variable url
    url_inst = f"https://{device_ip}/restconf/data/ietf-routing:routing/routing-instance"
    url_add_rt = f"https://{device_ip}/restconf/data/ietf-routing:routing/routing-instance={inst_name}/routing-protocols/routing-protocol=ietf-routing:static,1/static-routes/ietf-ipv4-unicast-routing:ipv4/route" 


    # Payload pour ajouter une instance
    payload_inst = {
        "ietf-routing:routing-instance":[
        {
            "name": f"{inst_name}",
            "routing-protocols": {
                "routing-protocol": [
                    {
                        "type": "ietf-routing:static",
                        "name": "1"
                    }
                ] 
            }
        }
      ]
    }   


    # Payload pour ajouter une route
    # ietf-ipv4-unicast-routing, ce module agrémente ietf-routing.
    payload_route = {
        "ietf-ipv4-unicast-routing:route": [
            {
                "destination-prefix": dest_net,
                "next-hop": {
                    "next-hop-address": next_hop
                }
            }
        ]
    }   


    # crée une intance VRF si elle n'existe pas.
    def manage_instance():
        try:
            response = requests.get(url_inst, auth=(username, password), headers=headers, verify=False) 
            response.raise_for_status()   
            data = response.json()
            instances = data["ietf-routing:routing-instance"]
        except requests.HTTPError as e:
            print(e)    

        # return pour stopper la fonction si ça match
        for instance in instances:
            if inst_name == instance["name"] :
                print(f"instance {inst_name} already exist")
                return

        try:
            response = requests.patch(url_inst, auth=(username, password), headers=headers, json=payload_inst, verify=False)
            response.raise_for_status()
            print(response.status_code)
            print(f"instance {inst_name} created")
        except requests.HTTPError as e:
            print(e)




    # ajoute une route statique à une instance
    def add_st_route():
            try:
                response = requests.patch(url_add_rt, auth=(username, password), headers=headers, json=payload_route, verify=False)
                response.raise_for_status()
                print(response.status_code)
                print(f"route {dest_net}, created in instance {inst_name}")
            except requests.HTTPError as e:
                print(e)    



    manage_instance()
    add_st_route()


# evite que le script ce déclenche à l'import    
if __name__ == "__main__":
    main()

   
