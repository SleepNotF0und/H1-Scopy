import requests,os,base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Edit hacker and token with your handle and api token , or create auth.txt including  this format  username:token   
# Edit hacker and token with your handle and api token , or create auth.txt including  this format  username:token   
list_my_programs=True
bounty_only=True
scope_only=True
hacker = ''
token = ''
print_assets_only=True
filtered_types=['URL','WILDCARD'] #,'OTHER']
#['AI_MODEL','APPLE_STORE_APP_ID','CIDR','DOWNLOADABLE_EXECUTABLES','GOOGLE_PLAY_APP_ID','HARDWARE','OTHER',
#'OTHER_APK','OTHER_IPA','SMART_CONTRACT','SOURCE_CODE','TESTFLIGHT','URL','WILDCARD','WINDOWS_APP_STORE_APP_ID']

asset_counter=0
def is_matching_type(mytypes,asset_type):
    try:
        if any(mytypes):
            if any("*" == str(item) for item in mytypes):
                return True            
            if any(asset_type.lower() == item.lower() for item in mytypes):
                return True
            return False
        else:
            return True
    except Exception as ex:
        input(f"Errors  for [{str(asset_type)}]{str(ex)}")
    return False
def read_credentials_from_file():
    try:
        if not os.path.exists('auth.txt'):
            return None, None
        with open('auth.txt', "r") as file:
            first_line = file.readline().strip()
        username, password = first_line.split(":", 1)
        return username, password
    except FileNotFoundError:
        return None, None
        
def get_after(original_string, target_substring):
    index = original_string.find(target_substring)
    if index != -1:
        return original_string[index + len(target_substring):]
    else:
        return ""
        
def get_before(original_string, target_substring):
    index = original_string.find(target_substring)
    if index != -1:
        return original_string[:index]
    else:
        return original_string
        
def read_lines_to_set(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        lines_set = set(lines)
        return lines_set
    except FileNotFoundError:
        return set()
        
def print_banner():
    global list_my_programs,bounty_only,scope_only,filtered_types
    print(("-"*88))
    print(f"[-]HacKerone -list_my_programs:{list_my_programs} -bounty_only:{bounty_only} -scope_only:{scope_only} RequiredAssers{filtered_types}\n")
    print("-----------------  exception@wearehackerone.com  --------------------------------------")
    print(("-"*88))

def basic(username,password):
    credentials = f"{username}:{password}"
    return base64.b64encode(credentials.encode()).decode()
    
def remove_duplicates_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        unique_lines = set()
        for line in lines:
            unique_lines.add(line.strip())
        with open(file_path, "w") as file:
            for unique_line in unique_lines:
                file.write(unique_line + "\n")

        
    except FileNotFoundError:
        pass    
def checkFile(filename):
    try:
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                # print(f'[-]{filename} Exists')
                pass  
    except Exception as e:
        print(f"[-]Error {filename}")
def file_append_list(file,list):
    joined_string = "\n".join(list)
    # print(f'[-]Saved Lines{len(list)} To file {file}')
    with open(file, "a") as file:
        file.write("\n"+joined_string)
        
def auth_failed():
    print("Authentication Failed Please input your credentials")
    exit(0)
def get_programs(hacker,token):
    auth=basic(hacker,token)
    if len(auth)<50:
        auth_failed()
        
    #/v1/hackers/programs?page[number]=" + page_number + "&page[size]=
    page=0
    programs=[]
    while True:
        page+=1
        url=f'https://api.hackerone.com/v1/hackers/programs?page[number]={page}&page[size]=99'
        headers = {"Accept": "application/json",
        "Connection": "close", "Authorization": "Basic "+auth}
        r=requests.get(url, headers=headers,verify=False)
        #print(r.text)
        print(f'[-]-Programs:{len(programs)} -Page{page} -Requesting : {url}')
        pcs=r.text.split('"handle":')
        found=0        
        for p in pcs:
            if p.startswith('"'):
                result = p.split(",")[0].strip('"')
                programs.append(result)
                found+=1
        if(found==0) or r.status_code!=200:
            file_append_list('programs.txt',programs)
            break;
            
    remove_duplicates_from_file('programs.txt')
def dec(s,l):
    return s+(' '*(l-len(s)))
def get_program_asset(auth,program):
    global bounty_only,scope_only,filtered_types,asset_counter,print_assets_only
    url=f'https://api.hackerone.com/v1/hackers/programs/{program}'
    headers = {"Accept": "application/json",
        "Connection": "close", "Authorization": "Basic "+auth}
    response=requests.get(url, headers=headers,verify=False)
    response_json = response.json()
    data_array = response_json.get("relationships", {}).get("structured_scopes", {}).get("data", [])
    assets=[]
    if response.status_code!=200:
        auth_failed()
    for item in data_array:
        asset_counter+=1
        asset_identifier = item.get("asset_identifier")
        asset_type= item.get("asset_type")
        #input(str(item))
        if bounty_only and "eligible_for_bounty': False" in str(item):
            continue
        if  not bounty_only and  scope_only and "eligible_for_submission': False" in str(item):
            continue
        if not asset_identifier:
            asset_identifier=get_before(get_after(str(item),"asset_identifier': '"),',').strip("'")
            asset_type=get_before(get_after(str(item),"asset_type': '"),',').strip("'")
        if is_matching_type(filtered_types,asset_type) is False:
            continue
        if not asset_type:
            asset_type=get_before(get_after(str(item),"asset_type': '"),',').strip("'")
        idx= '' if  print_assets_only else f'[{asset_counter}][{dec(asset_type+"]",25)}\t '
        as_id=f'\033[92m\t{idx}{asset_identifier}'
        print(as_id)
        assets.append(asset_identifier)
    os.makedirs(f"programs/{program}/", exist_ok=True)
    checkFile(f"programs/{program}/assets.txt")
    file_append_list(f"programs/{program}/assets.txt",assets)
    file_append_list(f"assets.txt",assets)
    
def get_assets():
    global print_assets_only
    auth=basic(hacker,token)
    programs=read_lines_to_set('programs.txt')
    #print(f"[-]Found {len(programs)}")
    if len(auth)<50:
        return
    for p in programs:
        if not print_assets_only:
            print(f'\033[96mQuering {p.strip()}:')
        get_program_asset(auth,p.strip())

if __name__ == "__main__":
    
    try:  
        os.makedirs("programs/", exist_ok=True)
        print_banner()
        if not hacker  or not token:
            hacker,token=read_credentials_from_file()
            print("Reading cred from file")
        checkFile("programs.txt")
        checkFile("assets.txt")
        if list_my_programs:
            get_programs(hacker,token)
        get_assets()
    except KeyboardInterrupt:
        print("\n\n\n[-]Leaving..........")
        exit()
