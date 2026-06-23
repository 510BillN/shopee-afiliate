from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Ban se thay the chuoi nay bang Cookie lay tu trinh duyet sau
SHOPEE_COOKIE = "DIEN_COOKIE_CUA_BAN_VAO_DAY"
SHOPEE_GRAPHQL_URL = "https://affiliate.shopee.vn/api/v1/graphql"

def get_shopee_short_link(original_url, sub_id_1="instagram"):
    headers = {
        "Cookie": SHOPEE_COOKIE,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
        data = response.json()
        if "data" in data and data["data"]["generateShortLink"]:
            return data["data"]["generateShortLink"]["shortLink"]
        return None
    except Exception as e:
        print("Loi: ", e)
        return None

# Route moi: Hien thi giao dien web cho nguoi dung
@app.route('/')
def home():
    return render_template('index.html')

# Route cu: API xu ly viec tao link
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
