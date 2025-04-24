import requests

cookies = {
    "PHPSESSID": "5efefmm3i6cj8306pt3k1l14bt",
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

params = {
    "_": "1743686975009",
}


for i in range(5, 10):
    # url = f"https://bircpc.ir/jury/users/{i}/delete"
    url = f"https://bircpc.ir/jury/teams/{i}/delete"
    print(url)
    response = requests.post(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
