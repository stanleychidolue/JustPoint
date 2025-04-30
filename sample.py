import requests
import os
import base64

client_id = os.environ.get('CLIENT_ID')
secret_key = os.environ.get('CLIENT_SECRET')
print(client_id)
print(secret_key)
# Concatenate with a colon
concatenated_string = f"{client_id}:{secret_key}"

# Encode to Base64
encoded_bytes = base64.b64encode(concatenated_string.encode("utf-8"))
encoded_string = encoded_bytes.decode("utf-8")

# Output the Base64 encoded string
print("Base64 Encoded String:", encoded_string)
BASE64_ENCODED_STRING = encoded_string   # should be located in .env file


url = "https://passport.k8.isw.la/passport/oauth/token?grant_type=client_credentials"

headers = {
    "accept": "application/json",
    "Authorization": f"Basic {BASE64_ENCODED_STRING} ",
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, headers=headers)

res = response.json()
print(res)
# print(response.text)
TOKEN = res.get('access_token')


url = f"https://qa.interswitchng.com/quicktellerservice/api/v5/services"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Terminalid": os.environ.get("TEST_TERMINAL_ID"),
    "Content-Type": "application/json"

}
try:
    res = requests.get(url, headers=headers)
except:
    print('an error occured')
print(res.text)
print(res.status_code)
# print(res.json())
if res.status_code == 200:
    dict_result = res.json()
    categories = dict_result.get('data')
    print(categories)
