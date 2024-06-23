import requests
import json
import re
from getpass import getpass






username = ""                                      #input("Hackerone username: ").strip()
token = ""      #getpass(f"{username} token: ").strip()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Hello": "HackerOne!",
}

AuthRequest = requests.session()
AuthRequest.auth = (username, token)
AuthRequest.headers.update(headers)


page =0
programs=[]

while True:
    page +=1
    
    URL = f'https://api.hackerone.com/v1/hackers/programs?page[number]={page}'

    Req = AuthRequest.get(URL, verify=True)
    filter_handle = Req.text.split('"handle":')
    
    found = 0
    for p in filter_handle:
        if p.startswith('"'):
            Result = p.split(",")[0].strip('"')
            programs.append(Result)
            found +=1

    if(found==0) or Req.status_code!=200:
        print("Programs Finished")
        break


assets = []
pro = 0
while pro <= len(programs):
    
    URL2 = f'https://api.hackerone.com/v1/hackers/programs/{programs[pro]}/structured_scopes'

    Req2 = AuthRequest.get(URL2, verify=True)
    filter_asset = Req2.text.split('"asset_identifier":')

    found2 = 0
    for f in filter_asset:
        if f.startswith('"'):
            Result2 = f.split(",")[0].strip('"')
            assets.append(Result2)
            found2 +=1
            pro +=1

    if(found2==0) or Req2.status_code!=200:
        print("Assets Finished Or Error")
        break   


print(assets)

Final = str(set(assets)).replace(']','').replace('[','').replace("'","").replace(',','\n').replace('"','').replace('}','').replace('{','')
with open("Results.txt", "w") as file:
    print("Results Saved in Results.txt, enjoy")
    file.write(Final)
