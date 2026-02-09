import requests
import json
import os
from dotenv import load_dotenv
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
        print("  ------------------------------------------------------------------------")
        print(" |  path doesn't exist, please restart the script provide a valid path.  |")
        print("  ------------------------------------------------------------------------")
        # (1) pour signaler qu'il y a eu une erreur au système
        sys.exit(1)

    # chargement des variables d'environnements
    load_dotenv(cred_path_ft)

    base_url = "https://api.meraki.com/api/v1"
    org_url = "/organizations"
    api_tokn = os.getenv("token")
    if not api_tokn:
        print("Missing api_tokn in .env file")
        sys.exit(1)

    # X-Cisco-Meraki-API-Key: <MERAKI_API_KEY> pour clé statique (legacy), bearer ok pour Oauth et clé statique (pour simplifier/unifier)
    headers = {
        "Authorization": f"Bearer {api_tokn}"
    }

    # permet de récupérer diverses informations (orga, networks, clients....)
    def get_things(url):
        try:
            response = requests.get(base_url + url, headers=headers, verify=False)
            response.raise_for_status()
            print(response.status_code)
            data = response.json()
            return data
        
        except requests.HTTPError as e:
            print(e)


    # récupère le nom et l'id de/s organisation/s
    orga_list = get_things(org_url)
    print("------------------------------------------------------------------------------")
    for orga in orga_list:
        print(f"{orga['name']}: {orga['id']}")
    print("------------------------------------------------------------------------------")
    print("This script retrieve clients or/and devices information into the network of your choice")
    org_id = input("copy the ID of the desired organization: ")
    print("------------------------------------------------------------------------------")


    # récupère le nom et l'id de/s réseau/x de l'organisation choisi
    net_url = f"/organizations/{org_id}/networks"
    netks = get_things(net_url)
    print("------------------------------------------------------------------------------")
    for network in netks:  
        print(f"{network['name']}: {network['id']}")
    print("------------------------------------------------------------------------------")
    net_id = input("copy the ID of the desired network: ")
    print(f"Enter 1 to display clients informations of this network.")
    print(f"Enter 2 to display devices informations of this network.")
    print("Enter 3 for both.")
    query = input("enter 1, 2 or 3: ")
    print("------------------------------------------------------------------------------")

    # récupère les infos sur les périphériques ou/et les clients du réseau choisi
    def retrieve_clients_devices(query):
        if query == "1":
            dvc_url = f"/networks/{net_id}/clients"
            dvc = get_things(dvc_url)
            print(f"there is {len(dvc)} client(s)")
            dvc_ft = json.dumps(dvc, indent=4)
            print("----------------------------------------------------------------------------")
            print(dvc_ft)
        elif query == "2":
            cli_url = f"/networks/{net_id}/devices"
            cli = get_things(cli_url)
            print(f"there is {len(cli)} device(s)")
            cli_ft = json.dumps(cli, indent=4)
            print("----------------------------------------------------------------------------")
            print(cli_ft)
        else:
            dvc_url = f"/networks/{net_id}/clients"
            dvc = get_things(dvc_url)
            print(f"there is {len(dvc)} client(s)")
            dvc_ft = json.dumps(dvc, indent=4)
            print("----------------------------------------------------------------------------")
            print(dvc_ft)  

            cli_url = f"/networks/{net_id}/devices"
            cli = get_things(cli_url)
            print(f"there is {len(cli)} device(s)")
            cli_ft = json.dumps(cli, indent=4)
            print("----------------------------------------------------------------------------")
            print(cli_ft)


    retrieve_clients_devices(query)

# evite que le script ce déclenche à l'import    
if __name__ == "__main__":
    main()

