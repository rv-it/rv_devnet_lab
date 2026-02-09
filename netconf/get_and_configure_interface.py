from ncclient import manager
from ncclient.operations import RPCError
import os
from dotenv import load_dotenv
import urllib3
from pathlib import Path
import sys
from xml.dom.minidom import parseString

def main():
    # désactive l'alerte généré par verify=False (ok pour lab)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
      
    # chemin vers le fichier contenant les variables d'envirronements
    cred_path = input("enter the path of your .env file (ex: path/to/file.env or C:\\path/to/file.env): ")
    cred_path_ft = Path(cred_path)  

    if not cred_path_ft.exists():
        print("  --------------------------------------------------------------------------")
        print(" |  path doesn't exist, please restart the script and provide a valid path. |")
        print("  --------------------------------------------------------------------------")
        # (1) pour signaler qu'il y a eu une erreur au système
        sys.exit(1) 

    # chargement des variables d'environnements
    load_dotenv(cred_path_ft)
    # Récupération des identifiants pour récuprer le token
    username = os.getenv("username")
    password = os.getenv("password")  

    # Détails du script et device cible
    print("This script retrieve interfaces info of your catalyst 8k, and then you can configure an ipv4/netmask on the interface")
    print("you can chose a loopback address if it doesn't exist, it will be created")
    target_host = input("Enter the target host ip without mask (ex: 10.10.10.2): ") 

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
            # avec subtree, affiche le sous arbre de ce module
            filter_xml = """
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
            """
            response = m.get_config(source="running", filter=("subtree", filter_xml))
            data_ft = parseString(response.xml).toprettyxml(indent="  ") # indent="  " ajoute/retire 2 espace à chaque niveau hiérarchique
            print("  --------------------------------")
            print(" | Details of available interfaces |")
            print("  --------------------------------")
            print(data_ft)
        except RPCError as e:
            print(f"/!\ NETCONF error : {e}") 

    # variable pour le XML de configuration
    user_choice = input("Enter yes if you want to update an interface (anything else to leave): ")
    if user_choice == "yes":
        int_name = input("enter/copy the interface name (ex: GigabitEthernet3): ")
        if int_name.startswith("GigabitEthernet"):
            int_type = "ianaift:ethernetCsmacd"
        elif int_name.startswith("Loopback"):
            int_type = "ianaift:softwareLoopback"
        else:
            print("invalid interface name or the script may need to be adapted to the target device interfaces")
            sys.exit(1)    
        int_ip = input("enter ip address (ex: 10.10.10.10): ")
        int_mask = input("enter netmask (ex: 255.255.255.0): ")
    else:
        print("script ended")
        # 0 car on pas une erreure (choix volontaire)
        sys.exit(0) 

    # XML pour configurer un interface
    config_data = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{int_name}</name>
          <description>configured with netconf and ietf</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">{int_type}</type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>{int_ip}</ip>
              <netmask>{int_mask}</netmask>
            </address>
          </ipv4>
          <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
        </interface>
      </interfaces>
    </config>"""  
    
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
            response = m.edit_config(target="running", config=config_data)
            print(response)
            print(f"{int_name} updated/created")
        except RPCError as e:
            print(f"/!\ NETCONF error : {e}")

if __name__ == "__main__":
    main()