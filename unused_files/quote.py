import json
import requests
import logger

log = logger.createLogger()


def get_quote():
    url = "https://api.quotable.io/random"

    try:
        response = requests.get(url)
        log.info("Successfully requested quote")
    except:
        log.info("Error while calling API...")
    res = json.loads(response.text)
    print(res)
    return res["content"] + "-" + res["author"]
