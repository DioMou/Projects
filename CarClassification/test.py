import requests
import json
url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp12-grader"
payload = {
            "accountId": 398543646162,
            "submitterEmail": 'lmou2@illinois.edu',
            "secret": 'uogQ6MM7owdc8muW',
            "ipaddress": '54.146.3.216:5000'
    }
r = requests.post(url, data=json.dumps(payload))
print(r.status_code, r.reason)
print(r.text)
