import requests
import os
import json
from concurrent.futures import ThreadPoolExecutor

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
STATE_FILE = "state.json"

HEADERS = {
 "User-Agent": "Mozilla/5.0",
 "Accept-Language": "ja-JP"
}

sites = [

 {"name":"クーリア①","url":"https://qlia.shop/?pid=187368266","type":"qlia"},
 {"name":"クーリア②","url":"https://qlia.shop/?pid=187368269","type":"qlia"},
 {"name":"クーリア③","url":"https://qlia.shop/?pid=187368267","type":"qlia"},
 {"name":"クーリア④","url":"https://qlia.shop/?pid=187368265","type":"qlia"},
 {"name":"クーリア⑤","url":"https://qlia.shop/?pid=185299628","type":"qlia"},
 {"name":"クーリア⑥","url":"https://qlia.shop/?pid=185299615","type":"qlia"},
 {"name":"クーリア⑦","url":"https://qlia.shop/?pid=187918895","type":"qlia"},
 {"name":"クーリア⑧","url":"https://qlia.shop/?pid=186116749","type":"qlia"},
 {"name":"クーリア⑨","url":"https://qlia.shop/?pid=187918894","type":"qlia"},
 {"name":"クーリア⑩","url":"https://qlia.shop/?pid=189151457","type":"qlia"},
 {"name":"クーリア⑪","url":"https://qlia.shop/?pid=189151455","type":"qlia"},
 {"name":"クーリア⑫","url":"https://qlia.shop/?pid=189151453","type":"qlia"},
 {"name":"クーリア⑬","url":"https://qlia.shop/?pid=189151447","type":"qlia"},
 {"name":"クーリア⑭","url":"https://qlia.shop/?pid=189151443","type":"qlia"},
 {"name":"クーリア⑮","url":"https://qlia.shop/?pid=189151445","type":"qlia"},
 {"name":"クーリア⑯","url":"https://qlia.shop/?pid=187918893","type":"qlia"},
 {"name":"クーリア⑰","url":"https://qlia.shop/?pid=187918892","type":"qlia"},
 {"name":"クーリア⑱","url":"https://qlia.shop/?pid=188589206","type":"qlia"},
 {"name":"クーリア⑲","url":"https://qlia.shop/?pid=188589205","type":"qlia"},
 {"name":"クーリア⑳","url":"https://qlia.shop/?pid=188589209","type":"qlia"},
 {"name":"クーリア㉑","url":"https://qlia.shop/?pid=187368262","type":"qlia"},
 {"name":"クーリア㉒","url":"https://qlia.shop/?pid=187368263","type":"qlia"},
 {"name":"クーリア㉓","url":"https://qlia.shop/?pid=187368257","type":"qlia"}

]

# 前回状態
try:
    with open(STATE_FILE,"r") as f:
        last_state=json.load(f)
except:
    last_state={}

new_state={}
notify=[]


def check(site):

    for _ in range(2):  # 2回試す
        try:

            r=requests.get(site["url"],headers=HEADERS,timeout=15)
            html=r.text

            available=False

            if "SOLD OUT" not in html:
                available=True

            return site,available

        except:
            continue

    return site,False


with ThreadPoolExecutor(max_workers=23) as executor:

    results=list(executor.map(check,sites))


for site,available in results:

    new_state[site["url"]]=available

    if available and not last_state.get(site["url"],False):

        notify.append(site)


if notify:

    msg="🔥在庫復活🔥\n\n"

    for n in notify:

        msg+=f"{n['name']}\n{n['url']}\n\n"

    payload={"content":msg}

    requests.post(WEBHOOK,json=payload)


with open(STATE_FILE,"w") as f:

    json.dump(new_state,f)
