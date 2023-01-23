# uvicorn main:app --host 0.0.0.0 --port 5001 --reload

from fastapi import FastAPI
import threading
import requests

app = FastAPI()


@app.get("/get-proxies-all")
async def get_proxies():
    url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data-with-geolocation.json"
    response = requests.get(url=url)
    dict_res = response.json()
    locations = [item['geolocation']['country'] for item in dict_res]
    ips = [item['ip'] for item in dict_res]
    ports = [item['port'] for item in dict_res]

    proxies = []
    results = [None] * len(ips)
    threads = [None] * len(ips)

    for index, (ip, port, location) in enumerate(zip(ips, ports, locations)):
        threads[index] = threading.Thread(
            target=is_proxy_alive_result, args=(ip, port, results, index))
        threads[index].start()

    for i in range(len(threads)):
        threads[i].join()

    for index, (ip, port, location, result) in enumerate(zip(ips, ports, locations, results)):
        if result:
            proxies.append({"ip": ip, "port": port, "location": location})

    data = {
        "total_proxies": len(proxies),
        "proxies": proxies
    }
    return data


@app.get("/get-proxies/{country}")
async def get_proxies(country):
    """ List available locations: ['Indonesia', 'United States', 'Pakistan', 'Japan', 'Venezuela', 'Peru', 'Hong Kong', 'Mexico', 'Brazil', 'Germany', 'Romania', 'Iran', 'Paraguay', 'France', 'Singapore', 'Armenia', 'Colombia', 'Poland', 'South Korea', 'Bangladesh', 'Chile', 'Greece', 'Dominican Republic', 'China', 'Mayotte', 'Nepal', 'Netherlands', 'Canada', 'Ukraine', 'Honduras', 'Taiwan', 'Philippines', 'Egypt', 'Thailand', 'India', 'Tanzania', 'Libya', 'Kazakhstan', 'Russia', 'Argentina', 'Nigeria', 'Ecuador', 'Turkey', 'Cyprus', 'Hungary']
    """
    url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data-with-geolocation.json"
    response = requests.get(url=url)
    dict_res = response.json()
    locations = [item['geolocation']['country'] for item in dict_res]
    ips = [item['ip'] for item in dict_res]
    ports = [item['port'] for item in dict_res]

    indices = [i for i, v in enumerate(locations) if v == country]

    if len(indices) == 0:
        return {
            "total_proxies": 0,
            "proxies": [],
            "available_countries": list(set(locations))
        }

    proxies = []
    for index, (ip, port, location) in enumerate(zip(ips, ports, locations)):
        if index in indices:
            proxies.append({"ip": ip, "port": port, "location": location})

    data = {
        "total_proxies": len(indices),
        "proxies": proxies,
        "available_countries": locations
    }
    return data


@app.get("/is-alive-proxy")
async def check_proxy(ip: str, port: str):
    if is_proxy_alive(ip, port):
        return 'Proxy is alive'
    return 'Proxy is dead'


def is_proxy_alive(ip, port):
    proxy = {'http': f'http://{ip}:{port}', 'https': f'http://{ip}:{port}'}

    try:
        response = requests.get('http://example.com', proxies=proxy, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def is_proxy_alive_result(ip, port, result, index):
    proxy = {'http': f'http://{ip}:{port}', 'https': f'http://{ip}:{port}'}

    try:
        response = requests.get('http://example.com', proxies=proxy, timeout=5)
        if response.status_code == 200:
            result[index] = True
            return True
        else:
            result[index] = False
            return False
    except requests.exceptions.RequestException:
        result[index] = False
        return False
