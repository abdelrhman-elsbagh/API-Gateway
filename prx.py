import urllib.request
import random
username = 'abdel9'
password = 'Admin_2050Pass'
entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
(username, password))
query = urllib.request.ProxyHandler({
'http': entry,
'https': entry,
})
execute = urllib.request.build_opener(query)
print(execute.open('https://ip.oxylabs.io/location').read())