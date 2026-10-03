from flask import Flask, render_template, request, jsonify
import requests
import re
import json
import os

app = Flask(__name__)
CONFIG_PATH = "config.json"

LANGS = {
    "zh-CN": {"name":"简体中文"},
    "zh-TW": {"name":"繁體中文"},
    "en": {"name":"English"},
    "ja": {"name":"日本語"},
    "ko": {"name":"한국어"},
    "ru": {"name":"Русский"},
    "fr": {"name":"Français"},
    "de": {"name":"Deutsch"},
    "es": {"name":"Español"},
    "pt": {"name":"Português"},
    "it": {"name":"Italiano"},
    "nl": {"name":"Nederlands"},
    "pl": {"name":"Polski"},
    "eo": {"name":"Esperanto"}
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"lang":"zh-CN","wiped":False}

def save_config(cfg):
    with open(CONFIG_PATH,"w",encoding="utf-8") as f:
        json.dump(cfg,f,ensure_ascii=False,indent=2)

def safe_calc(expr):
    if not re.fullmatch(r"[0-9+\-*/(). ]+",expr):
        return None
    try:
        res = eval(expr,{"__builtins__":{}},{})
        return str(res)
    except:
        return None

def baidu_search(keyword):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        url = f"https://www.baidu.com/s?wd={requests.utils.quote(keyword)}"
        r = requests.get(url,headers=headers,timeout=8)
        if r.status_code == 200:
            return url
        return None
    except:
        return None

def get_text(lang,key):
    texts = {
        "zh-CN":{"send":"发送","setting":"设置","delapp":"删除应用","confirm":"确认","cancel":"取消","searchhint":"搜索","calchint":"计算"},
        "zh-TW":{"send":"傳送","setting":"設定","delapp":"刪除應用","confirm":"確認","cancel":"取消","searchhint":"搜尋","calchint":"計算"},
        "en":{"send":"Send","setting":"Settings","delapp":"Delete App","confirm":"Confirm","cancel":"Cancel","searchhint":"Search","calchint":"Calculate"},
        "ja":{"send":"送信","setting":"設定","delapp":"アプリ削除","confirm":"確認","cancel":"キャンセル","searchhint":"検索","calchint":"計算"},
        "ko":{"send":"전송","setting":"설정","delapp":"앱 삭제","confirm":"확인","cancel":"취소","searchhint":"검색","calchint":"계산"},
        "ru":{"send":"Отправить","setting":"Настройки","delapp":"Удалить приложение","confirm":"Подтвердить","cancel":"Отмена","searchhint":"Поиск","calchint":"Вычислить"},
        "fr":{"send":"Envoyer","setting":"Paramètres","delapp":"Supprimer l'app","confirm":"Confirmer","cancel":"Annuler","searchhint":"Recherche","calchint":"Calculer"},
        "de":{"send":"Senden","setting":"Einstellungen","delapp":"App löschen","confirm":"Bestätigen","cancel":"Abbrechen","searchhint":"Suchen","calchint":"Berechnen"},
        "es":{"send":"Enviar","setting":"Ajustes","delapp":"Borrar app","confirm":"Confirmar","cancel":"Cancelar","searchhint":"Buscar","calchint":"Calcular"},
        "pt":{"send":"Enviar","setting":"Configurações","delapp":"Apagar app","confirm":"Confirmar","cancel":"Cancelar","searchhint":"Pesquisar","calchint":"Calcular"},
        "it":{"send":"Invia","setting":"Impostazioni","delapp":"Elimina app","confirm":"Conferma","cancel":"Annulla","searchhint":"Cerca","calchint":"Calcola"},
        "nl":{"send":"Versturen","setting":"Instellingen","delapp":"App verwijderen","confirm":"Bevestigen","cancel":"Annuleren","searchhint":"Zoeken","calchint":"Berekenen"},
        "pl":{"send":"Wyślij","setting":"Ustawienia","delapp":"Usuń aplikację","confirm":"Potwierdź","cancel":"Anuluj","searchhint":"Szukaj","calchint":"Oblicz"},
        "eo":{"send":"Sendi","setting":"Agordoj","delapp":"Forigi Apon","confirm":"Konfirmi","cancel":"Nuligi","searchhint":"Serĉi","calchint":"Kalkuli"}
    }
    return texts[lang][key]

@app.route("/")
def index():
    cfg = load_config()
    return render_template("index.html",config=cfg,langlist=LANGS)

@app.route("/chat",methods=["POST"])
def chat():
    cfg = load_config()
    if cfg.get("wiped"):
        return jsonify({"reply":""})
    msg = request.json.get("msg","").strip()
    calc_res = safe_calc(msg)
    if calc_res is not None:
        return jsonify({"reply":calc_res})
    if msg.startswith("search "):
        kw = msg[7:].strip()
        link = baidu_search(kw)
        if link:
            return jsonify({"reply":link})
        else:
            return jsonify({"reply":"search failed"})
    return jsonify({"reply":msg})

@app.route("/setlang",methods=["POST"])
def setlang():
    cfg = load_config()
    newlang = request.json.get("lang","zh-CN")
    cfg["lang"] = newlang
    save_config(cfg)
    return jsonify({"ok":True})

@app.route("/wipe",methods=["POST"])
def wipe():
    cfg = load_config()
    cfg["wiped"] = True
    save_config(cfg)
    return jsonify({"ok":True})

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=False)
