from datetime import datetime

# import json
# import aionhttp
# import asyncio
import requests

url = "http://127.0.0.1:8000/application/video"

with requests.get(url, stream=True) as r:
    for chunk in r.iter_content(16):
        print("{}: {}".format(datetime.utcnow(), chunk))
