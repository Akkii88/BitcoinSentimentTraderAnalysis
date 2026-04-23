import requests

# Download Historical Trader Data
url1 = "https://drive.google.com/uc?id=1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs"
response1 = requests.get(url1)
with open("data/historical_data.csv", "wb") as f:
    f.write(response1.content)

# Download Fear Greed Index Data
url2 = "https://drive.google.com/uc?id=1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf"
response2 = requests.get(url2)
with open("data/fear_greed_index.csv", "wb") as f:
    f.write(response2.content)
