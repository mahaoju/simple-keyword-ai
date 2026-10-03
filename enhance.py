import requests
import re
import json
import os
from bs4 import BeautifulSoup

CHAT_LOG_PATH = "chatlog.json"

def load_chatlog():
    if os.path.exists(CHAT_LOG_PATH):
        with open(CHAT_LOG_PATH,"r",encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chatlog(log):
    with open(CHAT_LOG_PATH,"w",encoding="utf-8") as f:
        json.dump(log,f,ensure_ascii=False,indent=2)

def baidu_search_summary(keyword):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        url = f"https://www.baidu.com/s?wd={requests.utils.quote(keyword)}"
        r = requests.get(url,headers=headers,timeout=8)
        soup = BeautifulSoup(r.text,"html.parser")
        result_items = soup.select(".result-op")[:2]
        summary_list = []
        for item in result_items:
            title_tag = item.select_one("h3 a")
            abstract_tag = item.select_one(".c-abstract")
            if title_tag and abstract_tag:
                title = title_tag.get_text(strip=True)
                abstract = abstract_tag.get_text(strip=True)
                summary_list.append(f"{title}\n{abstract}")
        full_text = "\n\n".join(summary_list)
        return f"Link: {url}\n\n{full_text}"
    except Exception:
        return "search failed"
