import modal


app = modal.App("hello")
image = modal.Image.debian_slim().pip_install('requests')

@app.function(image=image)
def hello():
    import requests
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    # print(data)
    return f"Hello Your IP is {data['ip']} from {data['city']}, {data['country']}"