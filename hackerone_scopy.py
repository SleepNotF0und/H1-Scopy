import requests
import json
import re
from getpass import getpass






username = "0xr3dhunt"                                      #input("Hackerone username: ").strip()
token = "cqTJbVxlJDpfAx8JuJbKAHIoYrLsaUDrIuBg2iBJaHc="      #getpass(f"{username} token: ").strip()

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
endpoint = "programs"

programs = set()

page_number = 1
while True:
    response = self._get(endpoint, params={"page[number]": page_number})

    if not response["links"].get("next") or not response.get("data"):
        break
    else:
        page_number += 1

        programs.update(
            [
                HackerOneProgram.load_from_dict(program)
                for program in response["data"]
            ]
        )

return programs



all_programs = session.list_programs()

for asset in session.get_program(all_programs[0]):
    print(asset)
"""

"""
cqTJbVxlJDpfAx8JuJbKAHIoYrLsaUDrIuBg2iBJaHc=


{'data': [{'id': '13', 'type': 'program', 'attributes': {'handle': 'security',

https://api.hackerone.com/v1/hackers/programs/goldmansachs/structured_scopes

https://api.hackerone.com/v1/hackers/programs?page[number]=28

"""