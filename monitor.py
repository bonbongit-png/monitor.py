import requests
import os
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
STATE_FILE = "state.json"

HEADERS = {
 "User-Agent": "Mozilla/5.0",
 "Accept-Language": "ja-JP"
}

sites = [

 {"name":"クーリア①","url":"https://qlia.shop/?pid=187368266"},
 {"name":"クーリア②","url":"https://qlia.shop/?pid=187368269"},
 {"name":"クーリア③","url":"https://qlia.shop/?pid=187368267"},
 {"name":"クーリア④","url":"https://qlia.shop/?pid=187368265"},
 {"name":"クーリア⑤","url":"https://qlia.shop/?pid=185299628"},
 {"name":"クーリア⑥","url":"https://qlia.shop/?pid=185299615"},
 {"name":"クーリア⑦","url":"https://qlia.shop/?pid=187918895"},
 {"name":"クーリア⑧","url":"https://qlia.shop/?pid=186116749"},
 {"name":"クーリア⑨","url":"https://qlia.shop/?pid=187918894"},
 {"name":"クーリア⑩","url":"https://qlia.shop/?pid=189151457"},
 {"name":"クーリア⑪","url":"https://qlia.shop/?pid=189151455"},
 {"name":"クーリア⑫","url":"https://qlia.shop/?pid=189151453"},
 {"name":"クーリア⑬","url":"https://qlia.shop/?pid=189151447"},
 {"name":"クーリア⑭","url":"https://qlia.shop/?pid=189151443"},
 {"name":"クーリア⑮","url":"https://qlia.shop/?pid=189151445"},
 {"name":"クーリア⑯","url":"https://qlia.shop/?pid=187918893"},
 {"name":"クーリア⑰","url":"https://qlia.shop/?pid=187918892"},
 {"name":"クーリア⑱","url":"https://qlia.shop/?pid=188589206"},
 {"name":"クーリア⑲","url":"https://qlia.shop/?pid=188589205"},
 {"name":"クーリア⑳","url":"https://qlia.shop/?pid=188589209"},
 {"name":"クーリア㉑","url":"https://qlia.shop/?pid=187368262"},
 {"name":"クーリア㉒","url":"https://qlia.shop/?pid=187368263"},
 {"name":"クーリア㉓","url":"https://qlia.shop/?pid=187368257"}

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

    try:

        r=requests.get(site["url"],headers=HEADERS,timeout=15)
        html=r.text

        # ページ変化検知
        page_hash=hashlib.md5(html.encode()).hexdigest()

        available=False

        if "SOLD OUT" not in html:
            available=True

        return site,available,page_hash

    except:

        return site,False,None


with ThreadPoolExecutor(max_workers=23) as executor:

    results=list(executor.map(check,sites))


for site,available,page_hash in results:

    last=last_state.get(site["url"],{})

    new_state[site["url"]] = {
        "available":available,
        "hash":page_hash
    }

    # 在庫復活
    if available and not last.get("available",False):

        notify.append(("stock",site))

    # ページ更新
    elif page_hash and page_hash != last.get("hash"):

        notify.append(("update",site))


if notify:

    msg="🚨ページ変化または在庫復活🚨\n\n"

    for t,n in notify:

        if t=="stock":
            msg+="🔥在庫復活\n"

        else:
            msg+="🔄ページ更新\n"

        msg+=f"{n['name']}\n{n['url']}\n\n"

    payload={"content":msg}

    requests.post(WEBHOOK,json=payload)


with open(STATE_FILE,"w") as f:

    json.dump(new_state,f)
