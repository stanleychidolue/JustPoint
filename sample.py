import requests
import os
import base64

# client_id = os.environ.get('CLIENT_ID')
# secret_key = os.environ.get('CLIENT_SECRET')
# print(client_id)
# print(secret_key)
# # Concatenate with a colon
# concatenated_string = f"{client_id}:{secret_key}"

# # Encode to Base64
# encoded_bytes = base64.b64encode(concatenated_string.encode("utf-8"))
# encoded_string = encoded_bytes.decode("utf-8")

# # Output the Base64 encoded string
# print("Base64 Encoded String:", encoded_string)
# BASE64_ENCODED_STRING = encoded_string   # should be located in .env file


# url = "https://passport.k8.isw.la/passport/oauth/token?grant_type=client_credentials"

# headers = {
#     "accept": "application/json",
#     "Authorization": f"Basic {BASE64_ENCODED_STRING} ",
#     "Content-Type": "application/x-www-form-urlencoded"
# }

# response = requests.post(url, headers=headers)

# res = response.json()
# print(res)
# # print(response.text)
# TOKEN = res.get('access_token')


# url = f"https://qa.interswitchng.com/quicktellerservice/api/v5/services"

# headers = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Terminalid": os.environ.get("TEST_TERMINAL_ID"),
#     "Content-Type": "application/json"

# }
# try:
#     res = requests.get(url, headers=headers)
# except:
#     print('an error occured')
# print(res.text)
# print(res.status_code)
# # print(res.json())
# if res.status_code == 200:
#     dict_result = res.json()
#     categories = dict_result.get('data')
#     print(categories)

import uuid
import os

print(str(uuid.uuid4()))
print(uuid.uuid4())
print(os.environ.get("FLUTTER_API_KEY"))

# amount = "200"
# customer_id = "+23490803840303"
# item_code = "AT099"
# biller_code = "BIL099"

# url = f"https://api.flutterwave.com/v3/billers/{biller_code}/items/{item_code}/payment"
# ref_id = str(uuid.uuid4())

# payload = {
#     "country": "NG",
#     "customer_id": customer_id,
#     "amount": amount,
#     "reference": ref_id,
#     "callback_url": "https://webhook.site/5f9a659a-11a2-4925-89cf-8a59ea6a019a"
# }
# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X",
#     "Content-Type": "application/json"
# }

# res = requests.post(url, json=payload, headers=headers)
# print(res.status_code)
# if res.status_code == 200:
#     dict_result = res.json()
#     print(dict_result.get("data"))
#     # ref_id = 9300049404444

#     # confirm payment status
#     url = f"https://api.flutterwave.com/v3/bills/{ref_id}?verbose=1"
#     # url = f"https://api.flutterwave.com/v3/bills/{ref_id}"
#     param = {"verbose": 1}
#     response = requests.get(url, params=param, headers=headers)
#     print(response.status_code)
#     if response.status_code == 200:
#         response_dict = response.json()
#         data = response_dict.get('data')
#         print(data)
#         if data.get("code") == "200" and data.get("status") == "successful":
#             flw_ref = data.get("flw_ref")
#             tx_ref = data.get("tx_ref")
#             batch_id = data.get("batch_id")
#             transaction_date = data.get("transaction_date")
#             customer_reference = data.get("customer_reference")
#             amount = data.get("amount")
#             customer_id = data.get("customer_id")
#             product = data.get("product")

#             # safe this info to a DB table
#             # return redirect()
