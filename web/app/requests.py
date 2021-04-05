import requests
r = requests.get('http://10.0.0.67:9090/api/v1/query_range?query=temperature&start=1616993300&end=1617166100&step=20s')
print(r.text)
