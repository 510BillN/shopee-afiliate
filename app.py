from flask import Flask, request, jsonify, render_template
from curl_cffi import requests
import re

app = Flask(__name__)

# 1. DAN LAI COOKIE MOI NHAT CUA BAN VAO DUOI DAY (Giu nguyen 3 dau ngoac kep)
SHOPEE_COOKIE = """SPC_F=8YPpw60uPneGBcs5Wdow5JMItW0oXXIe; REC_T_ID=c40100c9-4bb5-11f1-bea6-b6a07e8f363a; SPC_SI=pDrvaQAAAABJa052cUhTSqvfCwMAAAAARHBYMTR3aFo=; language=vi; csrftoken=qEdS120pu2PgHdhOyOWp8MKwrmPxuSO6; SPC_CLIENTID=OFlQcHc2MHVQbmVHeryujkhanowabjdk; SPC_CDS_CHAT=268cbe73-3486-4f01-98fc-000aff1a3fdf; SPC_SC_SESSION=gmsRi+6aXijSaGvHJiRLhFULPtOvTbzIULRfoz3KG5FJU0ZldqY3ncZKFFFbXPmZuvnIvD5yM5LaQcVO8V59r1rLcNhJJSpIkCw6FWwIB9BdtetpvE5p083V/sivM34n1B2GYcGJeUVSntJMwQS91eqvGCbnjjO9QGZrxZeRX7Kmdp4OFBoCwlorLGa248toW2yP0p9dhSKpiQ5WbucUEoeS8JTVibC1SZyXt9iW1dgL9/4Ax8zCV5XQsiNbRk2KRZgOy1TB5bUPvpgYlNsYu+A==_1_800719113; SPC_SC_MAIN_SHOP_SA_UD=0; SPC_STK=8vN0TN/S9imH8DY5fYy7Zswsm16Bs0xbmVxH0hclTREYIfvtQcnIq9ZbBWuDt5Syl3HiuBBFE8oiQ5CTMxBYb2nIIJxp9zhVdquKaGWoKL4oH+DjiJBiHK4qZmjTMPfUxMgnzRzXiSCg3TfKS3B66tU4j2PnkjE4LQEMtV8x+txeTavPSlYVH6YBRvaJjRN6dQ62pcER9c6R3LEn3qGhp5Tibzpk0pW7DzT4dDNTWl0OZZvwzCbuWXc3+qsMtitBkAUQD7RyNi2YT2vsM1OHDfpQbpTE0BU20N5Inri+pW95GP0zMJLKZ41tRLWdfVOg2WAefs6lZz9Y76RiN5kObPL88ecaOCeBVcFH/lKia5Tr+8tSaNjZvXNd2E1k8VMIpOYTgAeUWgRkNPWLLK7xI03YEsV5Blz/XqNGVZwfNpRhMVZcbbQEiq2T/kcrQO3rLbQ4pYEqrodeDWvDx7RTmcAgOd9bsjRcar0dzLQX9jqROZMRub2/O9YngqUjjJbk; SC_DFP=nUnbheMkLyyZuzKlIrdsQDTPWOqeRHqF; CTOKEN=Atr13WrwEfGC8ZL2bVCWsw%3D%3D; language=vi; _QPWSDCXHZQA=3fcc9819-c97c-4b35-f84a-abea2397a687; REC7iLP4Q=35195b67-e360-476a-a1bc-ab8fd424f253; _sapid=8c8a2faefe2715c489d7e3ac6ce98b78085266512c0fccbbaa10eaa9; SPC_EC=Wk1yQzREYjdkeFN4MFF6U5vll+XYkxxkRtur9kttfPmqXdjxjslRtDDXc4be1Gy007kIEbr41eEMhxExca4UAe0xzpxGhEOxJFeCbdVJ2gnegJUXa77wCOusYrFHYDXvBfg4wjKvqHNQQNEpKgkvfKzjhAso//kvTPnkxHXyl0QWUmlEYBUaNXnBu6HKnp3Ms94a88f/hGUIZsMsoX/sCg==.ADYEnPR20e3EpgUNTzssR86dnOjPc6V0GMbHP9w3IPS3; SPC_ST=Sko4WDJ0TmxZQkJCTld0MIqQdgVZcgLTsooz2UkVIhoIbt6URw6aYVCz+FPdgsp6amzgRj8xpuFamIVrgn+hBpIO0PS+vu90w6VeP3UuaSfkDMmhUENiULxIM8lvsO9Pvlktq4Qu4Zp8SWsoir/cyc3aDY5M02Y+ZUte0/U3Aw5AR6HEnhOBrLZxYCOKC7B32zcgfjiIEYJpamtidAbiaw==.ALRG0bCnJREQaP95i4GwgcTs3/MBy8IqT8XPH0Lz7N4h; SPC_U=12571813908; SPC_R_T_ID=d6J+QukOLuFZhpX8sDOJyE+/54i2sGcYV/0y600LfTkfQ0U6Gr2MuOeMtZxBBsKxsgnfbQlaro59g5d7IfPt525DbinxAwyVPAlJjVeXX+f9miMYe/SJpzdrAqI/tAOdel/HNaqbFGVZjOgkqC9FmeSd3ndL9eCdKKWozH48Cno=; SPC_R_T_IV=WXRBS0lHeU94WlJqZ0kxRw==; SPC_T_ID=d6J+QukOLuFZhpX8sDOJyE+/54i2sGcYV/0y600LfTkfQ0U6Gr2MuOeMtZxBBsKxsgnfbQlaro59g5d7IfPt525DbinxAwyVPAlJjVeXX+f9miMYe/SJpzdrAqI/tAOdel/HNaqbFGVZjOgkqC9FmeSd3ndL9eCdKKWozH48Cno=; SPC_T_IV=WXRBS0lHeU94WlJqZ0kxRw==; sense_sa_r=s"""

SHOPEE_GRAPHQL_URL = "https://affiliate.shopee.vn/api/v1/graphql"

def get_shopee_short_link(original_url, sub_id_1="instagram"):
    # Tu dong lay chinh xac 100% token cho du co ky tu dac biet
    csrf_token = ""
    match = re.search(r'csrftoken=([^;]+)', SHOPEE_COOKIE)
    if match:
        csrf_token = match.group(1).strip()

    # Bo sung Header Origin bat buoc cua he thong Shopee Affiliate
    headers = {
        "Cookie": SHOPEE_COOKIE,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://affiliate.shopee.vn",
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
        # Su dung curl_cffi de gia lap TLS fingerprint cua Chrome 120, vuot WAF Shopee
        response = requests.post(SHOPEE_GRAPHQL_URL, json=payload, headers=headers, impersonate="chrome120")
        
        # In nguyen van cau tra loi cua Shopee ra log de bat benh neu co loi
        print("============== DEBUG SHOPEE ==============")
        print(f"HTTP Status: {response.status_code}")
        print(f"Raw Response: {response.text}")
        print("==========================================")

        try:
            data = response.json()
        except Exception as json_err:
            print("[-] Shopee khong tra ve JSON, co the bi chan: ", json_err)
            return None
        
        # Parse ket qua tra ve de trich xuat link rut gon
        if "data" in data and data["data"] and data["data"].get("generateShortLink"):
            return data["data"]["generateShortLink"]["shortLink"]
        else:
            return None
    except Exception as e:
        print("[-] Loi Request: ", e)
        return None

# Route hien thi giao dien web cho nguoi dung
@app.route('/')
def home():
    return render_template('index.html')

# Route API xu ly viec tao link
@app.route('/api/get-affiliate', methods=['GET'])
def api_get_affiliate():
    # Nhan tham so url (link goc) tu frontend
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Thieu tham so url"}), 400
        
    # Goi ham chuyen doi link va gan the instagram
    short_link = get_shopee_short_link(url, "instagram")
    
    if short_link:
        return jsonify({"status": "success", "affiliate_link": short_link})
    else:
        return jsonify({"status": "error", "message": "Khong the tao link"}), 500

if __name__ == '__main__':
    # Chay server
    app.run(host='0.0.0.0', port=5000)
