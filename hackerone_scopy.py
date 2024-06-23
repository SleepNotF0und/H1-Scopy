import requests
import json
import re
from getpass import getpass






username = "<<-Hackerone-USERNAME->>"                                      #input("Hackerone username: ").strip()
token = "<<-Hackerone-TOKEN->>"                                          #getpass(f"{username} token: ").strip()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Hello": "HackerOne!",
}

AuthRequest = requests.session()
AuthRequest.auth = (username, token)
AuthRequest.headers.update(headers)


for page in range(1,29):
    
    URL = f"https://api.hackerone.com/v1/hackers/programs?page[number]={page}"

    Req = AuthRequest.get(URL).json()
    

    filter_handle = re.match('handle', Req)
    print(filter_handle)



"""
Links to fetch assets

https://api.hackerone.com/v1/hackers/programs?page[number]=28
https://api.hackerone.com/v1/hackers/programs/<<-Program-Handle->>/structured_scopes

"""
