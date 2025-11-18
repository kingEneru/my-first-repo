import requests
import json

cert_content="""-----BEGIN CERTIFICATE-----
MIIH0zCCBrugAwIBAgIQQAGZb+kwtHHqt0AoLvtbUzANBgkqhkiG9w0BAQsFADBy
...
dKPXb49sPTb6td4A0qEzUpcaeHJbsGCAiG/4FjyS7DiCDCf0p2wv
-----END CERTIFICATE-----
"""

url = "https://decoder.link/api"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build=MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36 Edg/142.0.0.0"
}

payload = {
  "method": "ocsp",
  "params": {
    "user_input": cert_content
  }
}

# json=payload 会自动将 Python 字典序列化为 JSON 字符串，并设置 Content-Type 为 application/json
response = requests.post(url, headers=headers, json=payload)

# 检查 HTTP 响应状态码，如果不是 2xx，则抛出异常
response.raise_for_status()

print(f"请求成功！状态码: {response.status_code}")
print("响应内容 (JSON):")
# 尝试解析 JSON 响应并美化打印
print(json.dumps(response.json(), indent=2))
