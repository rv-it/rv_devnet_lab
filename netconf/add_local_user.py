from ncclient import manager
from ncclient.operations import RPCError
import getpass
import os
from dotenv import load_dotenv
import urllib3
from pathlib import Path
import sys


def main():
    # désactive l'alerte généré par verify=False (ok pour lab)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

    # chemin vers le fichier contenant les variables d'envirronements
    # si chemin windows: r"path\to\file"
    cred_path = input(r"enter the path of your .env file (ex: path/to/file.env or C:\\path\to\file.env): ")
    cred_path_ft = Path(cred_path)  

    if not cred_path_ft.exists():
        print("  ------------------------------------------------------------------------")
        print(" |  path doesn't exist, please restart the script and provide a valid path.  |")
        print("  ------------------------------------------------------------------------")
        # (1) pour signaler qu'il y a eu une erreur au système
        sys.exit(1) 

    # chargement des variables d'envirronements
    load_dotenv(cred_path_ft)
    # Récupération des identifiants pour récuprer le token
    username = os.getenv("username")
    password = os.getenv("password")  

    # Demande des informations utilisateur
    print("This script add a user with password and privilege in a cisco catalyst")
    target_host = input("Enter the target host ip without mask (ex: 10.10.10.2): ")
    new_user = input("Enter the username: ")
    privilege = input("Enter the privilege (1-15): ")
    pwd = getpass.getpass("Enter the password: ") 

    # XML pour ajouter un utilisateur
    config_data = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username>
          <name>{new_user}</name>
          <privilege>{privilege}</privilege>
          <secret>
            <secret>{pwd}</secret>
          </secret>
        </username>
      </native>
    </config>
    """ 


    # Connexion au switch via netconf (ncclient)
    with manager.connect(
        host=target_host,
        port=830,
        username=username,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m: 
        try:
            print("NETCONF connexion: OK")
            response = m.edit_config(target="running", config=config_data)
            print(f"user {new_user} added ")
            print(response)
        except RPCError as e:
            print(f"/!\ NETCONF error : {e}")

if __name__ == "__main__":
    main()
