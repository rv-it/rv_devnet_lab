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
        print("  --------------------------------------------------------------------------")
        print(" |  path doesn't exist, please restart the script and provide a valid path. |")
        print("  --------------------------------------------------------------------------")
        # (1) pour signaler qu'il y a eu une erreur au système
        sys.exit(1)

    # chargement des variables d'envirronements
    load_dotenv(cred_path_ft)
    # Récupération des identifiants pour récuprer le token
    username = os.getenv("username")
    password = os.getenv("password")    

    if not username or not password:
        print("Missing username or password in .env file")
        sys.exit(1)   

    print("-----------------------------------------------------------------------------------------------")
    print("this script retrieves running configuration of all devices from Cisco catalyst center,")
    print("then store the configuration files (running_hostname.txt) in the folder of your choice.")
    print("-----------------------------------------------------------------------------------------------")
    catalyst_ip = input("enter ip address of your Catalyst center without netmask (ex: 10.10.10.10): ")
    print("-----------------------------------------------------------------------------------------------")
    path_fold = input(r"path to store files (ex: c:\\path\folder or path/folder): ")
    path_fold_ft = Path(path_fold)
    print("-----------------------------------------------------------------------------------------------")    

    if not path_fold_ft.exists():
        print("  ------------------------------------------------------------------------")
        print(" |  path doesn't exist, please set a valid path and restart the script.  |")
        print("  ------------------------------------------------------------------------")
        # (1) pour signaler qu'il y a eu une erreur au système
        sys.exit(1)   

    url = f"https://{catalyst_ip}/dna"
    auth_url = "/system/api/v1/auth/token"
    dvc_url = "/intent/api/v1/network-device"   

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-auth-token": ""
    }   


    try:
      response = requests.post(url + auth_url, auth=(username,password), verify=False)
      response.raise_for_status()
      data = response.json()
      TKN = data["Token"]
      headers["x-auth-token"] = TKN
      # print(TKN)
    except requests.HTTPError as e:
      print(e)    

    # crée un dictionnaire vide et le rempli au format {"hostname1": "id"1, "hostname2": "id2"... }
    def retrieved_id_hostname():
      try:            
        response = requests.get(url + dvc_url, headers=headers, verify=False)
        response.raise_for_status()
        dvcs = response.json()
        dvcs_name_id = {}
        for dvc in dvcs["response"]:
          dvc_name = dvc["hostname"]
          dvc_id = dvc["id"]
          dvcs_name_id[dvc_name] = dvc_id
        return dvcs_name_id
      except requests.HTTPError as e:
        print(e)    

    dico_hostname_id = retrieved_id_hostname()    

    #  .items pour itérer sur les clés et les valeurs
    # récupère la running config et la sauvegarde dans un fichier
    for hostname, host_id in dico_hostname_id.items():
          # endpoint pour obtenir la running config
          url_details_by_id = f"/intent/api/v1/network-device/{host_id}/config"
          try:
            response = requests.get(url + url_details_by_id, headers=headers, verify=False)
            response.raise_for_status()
            data = response.json()
            dvc_run = data["response"]
            filename = f"running_{hostname}.txt"
            # path_fold_ft != string, objet Path, le / veut dire joindre les deux chemin (idem path_fold_ft.joinpath(filename) ).
            with open(path_fold_ft / filename, "w") as f:
              f.write(dvc_run)
            print(f"Config saved in : {path_fold_ft / filename}")
          except requests.HTTPError as e:
            print(e)    

if __name__ == "__main__":
   main()



