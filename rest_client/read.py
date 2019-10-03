import requests

if __name__ == "__main__":
    res = requests.get(
        url='http://127.0.0.1:5000/resource/t2'
    )
    print(res.status_code)
    print(res.json())

    res = requests.get(
        url='http://127.0.0.1:5000/resource/location/4th'
    )
    print(res.status_code)
    print(res.json())
