#Bulk pushing questions

questions = \
[
# [<Question>,<Question Category ID>]
 ["Question 1","2"],
 ["Question 2","1"],
]

import requests
for q in questions:
	r = requests.post("http://127.0.0.1/send", data={'question': q[0], 'categories': q[1]})
	print(r.status_code, r.reason)