from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__)

# 1. DAN LAI COOKIE CUA BAN VAO DUOI DAY (Giu nguyen 3 dau ngoac kep)
SHOPEE_COOKIE = """SPC_F=8YPpw60uPneGBcs5Wdow5JMItW0oXXIe; REC_T_ID=c40100c9-4bb5-11f1-bea6-b6a07e8f363a; SPC_SI=pDrvaQAAAABJa052cUhTSqvfCwMAAAAARHBYMTR3aFo=; language=vi; csrftoken=qEdS120pu2PgHdhOyOWp8MKwrmPxuSO6; SPC_CLIENTID=OFlQcHc2MHVQbmVHeryujkhanowabjdk; SPC_CDS_CHAT=268cbe73-3486-4f01-98fc-000aff1a3fdf; SPC_SC_SESSION=gmsRi+6aXijSaGvHJiRLhFULPtOvTbzIULRfoz3KG5FJU0ZldqY3ncZKFFFbXPmZuvnIvD5yM5LaQcVO8V59r1rLcNhJJSpIkCw6FWwIB9BdtetpvE5p083V/sivM34n1B2GYcGJeUVSntJMwQS91eqvGCbnjjO9QGZrxZeRX7Kmdp4OFBoCwlorLGa248toW2yP0p9dhSKpiQ5WbucUEoeS8JTVibC1SZyXt9iW1dgL9/4Ax8zCV5XQsiNbRk2KRZgOy1TB5bUPvpgYlNsYu+A==_1_800719113; SPC_SC_MAIN_SHOP_SA_UD=0; SPC_STK=8vN0TN/S9imH8DY5fYy7Zswsm16Bs0xbmVxH0hclTREYIfvtQcnIq9ZbBWuDt5Syl3HiuBBFE8oiQ5CTMxBYb2nIIJxp9zhVdquKaGWoKL4oH+DjiJBiHK4qZmjTMPfUxMgnzRzXiSCg3TfKS3B66tU4j2PnkjE4LQEMtV8x+txeTavPSlYVH6YBRvaJjRN6dQ62pcER9c6R3LEn3qGhp5Tibzpk0pW7DzT4dDNTWl0OZZvwzCbuWXc3+qsMtitBkAUQD7RyNi2YT2vsM1OHDfpQbpTE0BU20N5Inri+pW95GP0zMJLKZ41tRLWdfVOg2WAefs6lZz9Y76RiN5kObPL88ecaOCeBVcFH/lKia5Tr+8tSaNjZvXNd2E1k8VMIpOYTgAeUWgRkNPWLLK7xI03YEsV5Blz/XqNGVZwfNpRhMVZcbbQEiq2T/kcrQO3rLbQ4pYEqrodeDWvDx7RTmcAgOd9bsjRcar0dzLQX9jqROZMRub2/O9YngqUjjJbk; SC_DFP=nUnbheMkLyyZuzKlIrdsQDTPWOqeRHqF; CTOKEN=Atr13WrwEfGC8ZL2bVCWsw%3D%3D; SPC_EC=VHFYZ3ZXTGpHaTl1a1F1U/Epa6geq4amEqXMr55k9vLtJij48RfAd8/93FdmBT7HVojQx6C+FFCXgmRV4m77Scr62PuGBOX/gJPR6YVy9sEEEkaFwlb2JE9XR7oD6h90Z/+gddH4lzkNL8ytbIAT9GuaTFZsDe8cL6vrUToI+mTzjwbCSet4OPNj5v9GgHMlVPhfutM+01z0FLwoWaEatQ==.ABnoQP4dEgEq69Ga58CKyjlSuxBphNYrU8RlDbZNM5pp; SPC_ST=THJoQTBjWUc3SG9kWkZaVc2SvuSCiaHSDRW7+jzI3FG+uxeCQM5ureh8fx1c/7XZOqY1mAdZ2t5dJ4fe2EJPBhzrUTuBRJ/MOCWewakkelFZb598kD7bthCj6sVyUus/ctLvkvA0PE0johkLkRc95u8xpkBwoppf5RMvG7TFTrwM7rZtOVu1ZW/3bICKPGX1g9HZ9IbnvTNUpNylQVM+Xw==.AMNFsZdSlf2Gsoig6N3f8bJ/7TZNePV5wQcbD3CT/R5R; SPC_U=800719113; SPC_T_IV=WnI4Mzc3ZFZxblVCbHlTZQ==; SPC_R_T_ID=/nMf1/KvAY+o30/PbqhqUHO8Ew7LgxFt3wA2+qFDng13LeZNarnGCxBtVcj8+dFqIqlN1xvZFjcQdz00q0ANZd7wqFJAfLLyQgFB+HakjjiRgX3IFosq+kL0tVDxXO7ZQqzfrlDLdD6MjZ848I6BVCuL8TrfTWsGZkrs22WEtZ4=; SPC_R_T_IV=WnI4Mzc3ZFZxblVCbHlTZQ==; SPC_T_ID=/nMf1/KvAY+o30/PbqhqUHO8Ew7LgxFt3wA2+qFDng13LeZNarnGCxBtVcj8+dFqIqlN1xvZFjcQdz00q0ANZd7wqFJAfLLyQgFB+HakjjiRgX3IFosq+kL0tVDxXO7ZQqzfrlDLdD6MjZ848I6BVCuL8TrfTWsGZkrs22WEtZ4=; sense_sa_r=s; language=vi; _QPWSDCXHZQA=3fcc9819-c97c-4b35-f84a-abea2397a687; REC7iLP4Q=35195b67-e360-476a-a1bc-ab8fd424f253; _sapid=8c8a2faefe2715c489d7e3ac6ce98b78085266512c0fccbbaa10eaa9"""

SHOPEE_GRAPHQL_URL = "https://affiliate.shopee.vn/api/v1/graphql"

def get_shopee_short_link(original_url, sub_id_1="instagram"):
    csrf_token = ""
    match = re.search(r'csrftoken=([a-zA-Z0-9]+)', SHOPEE_COOKIE)
    if match:
        csrf_token = match.group(1)

    headers = {
        "Cookie": SHOPEE_COOKIE,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Referer": "https://affiliate.shopee.vn/dashboard",
        "X-CSRFToken": csrf_token
    }
    
    payload = {
        "query": "mutation generateShortLink($input: GenerateShortLinkInput!) { generateShortLink(input: $input) { shortLink } }",
        "variables": {
            "input": {
                "originUrl": original_url,
                "subIds": [sub_id_1]
            }
        }
    }
    
    try:
        response = requests.post(SHOPEE_GRAPHQL_URL, json=payload, headers=headers)
        
        # IN NGUYEN VAN CAU TRA LOI CUA SHOPEE RA LOG DE BAT BENH
        print("============== DEBUG SHOPEE ==============")
        print(f"HTTP Status: {response.status_code}")
        print(f"Raw Response: {response.text}")
        print("==========================================")

        try:
            data = response.json()
        except Exception as json_err:
            print("[-] Shopee khong tra ve JSON, co the bi chan: ", json_err)
            return None
        
        if "data" in data and data["data"] and data["data"].get("generateShortLink"):
            return data["data"]["generateShortLink"]["shortLink"]
        else:
            return None
    except Exception as e:
        print("[-] Loi Request: ", e)
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-affiliate', methods=['GET'])
def api_get_affiliate():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Thieu tham so url"}), 400
        
    short_link = get_shopee_short_link(url, "instagram")
    
    if short_link:
        return jsonify({"status": "success", "affiliate_link": short_link})
    else:
        return jsonify({"status": "error", "message": "Khong the tao link"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
