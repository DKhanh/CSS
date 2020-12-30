import http.client
import pprint
import json

# connection = http.client.HTTPSConnection("api.plos.org")
# connection.request("GET", "/search?q=title%3ADNA")
# response = connection.getresponse()
# headers = response.getheaders()
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint("Headers: {}".format(headers))
# print("")
# print("")
# pp.pprint(response.length)
# pp.pprint(response.read().decode())

conn = http.client.HTTPSConnection('www.httpbin.org')
headers = {'Content-type': 'application/json'}
foo = {"FileFullName": "all_log.txt", "NumberOfStep": 5, "AuxiPath": [{"Left": "7e2e63972baa7510684eaf54fc369f99013c0bc6c81111e8c01f3a57b7a43d05", "Right": "8afe46e5160e53577588d05d0983ea01ce4be911b330fea7bdeab498f17a8651"}, {"Left": "fd713f1d3a073275c892c32455d07d830f554596d4083cdceb8fdd038a5d0078", "Right": "NULL"}, {"Left": "NULL", "Right": "6c22864a4e737621229d876e7c30df40a8627cc012f6707c1ef1ec99a363f4f1"}, {"Left": "NULL", "Right": "e94909814c93f937819f1c7145eb8a49556e5b43e33851ded3ee5879c2043a22"}, {"Left": "NULL", "Right": "303c7dca4983a97183f90cbf986b0bf0f6429a9716853430ffb0d5c33416789d"}]}
json_data = json.dumps(foo)

conn.request('POST', '/post', json_data, headers)
response = conn.getresponse()
print(response.read().decode())

# Establishing connection with SERVER_ADDR/SERVER_URL
Connection = http.client.HTTPSConnection(SERVER_ADDR)
Connection.request("GET", SERVER_URL)

# Preparing json data to send out
Headers = {"Content-type": "Application/json"}
OutputToBc = ReturnAuxiPath(FileAddress, 2)
JsonData = json.dump(OutputToBc)

# Creating request to server
Connection.request("POST", "/post", JsonData, Headers)
Response = Connection.getresponse()
print(response.read().decode())


import json
from urllib.request import urlopen

data = {"text": "Hello world github/linguist№1 **cool**, and #1!"}
response = urlopen("http://host.docker.internal:3000/checkData", json.dumps(data).encode())
print(response.read().decode())


url = 'http://host.docker.internal:3000/checkData'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, data = myobj)

#print the response text (the content of the requested file):

print(x.text)