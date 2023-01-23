## 1. Simple Fast API to crawl the proxies

Reference: https://github.com/mertguvencli/http-proxy-list

`http-proxy-list` github: It is a lightweight project that, every 10 minutes, scrapes lots of free-proxy sites, validates if it works, and serves a clean proxy list.

However, after several minutes, a lot of proxies are dead. I want to create the simple API using FastAPI to crawl all the proxies `http-proxy-list` project and check all the available proxies up to now.


- `get-proxies-all`: Get only available proxies (still alive)
- `get-proxies/{country}`: Get proxy by country name
- `is-alive-proxy`: To check whether one proxy is alive or dead



## 2. How to run application
```bash
uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

## 3. Fast API Documentation
![Alt text](CleanShot%202023-01-23%20at%2023.59.07.png)

