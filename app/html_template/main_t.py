import requests
import json

response = requests.get("https://www.emag.ro/search/iphone%209%20plus?ref=effective_search")

print('Status code: ' + str(response.status_code))

json_string_repr = json.dumps(response.content.decode('utf-8'))
my_json = json.loads(json_string_repr)
print(my_json[0])

# Writes the HTML to a file
#
# with open('dummy.html', 'wb') as file:
#     for line in response.iter_content(1024):
#         file.write(line)