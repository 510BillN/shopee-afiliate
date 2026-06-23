from flask import Flask, request, jsonify, render_template
from curl_cffi import requests
import re

app = Flask(__name__)

# 1. DAN LAI COOKIE MOI NHAT CUA BAN VAO DUOI DAY (Giu nguyen 3 dau ngoac kep)
SHOPEE_COOKIE = """DAN_TOAN_BO_COOKIE_CUA_BAN_VAO_DAY"""

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
