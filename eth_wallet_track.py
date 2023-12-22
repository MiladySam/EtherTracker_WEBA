from requests import get
from matplotlib import pyplot as plt
from datetime import datetime


API_KEY = "CUUXI6S5B5HETZPC29XJ4SEUCYD4ZH7E6I"

address = "0xDDD0Bc1144f64d717C66AC8B4247045bB5a8A1d1"

ETHER_VALUE = 10**18


BASE_URL = "https://api.etherscan.io/api"

def api_en_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"


    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

def get_compte_balance(address):
    balance_url = api_en_url("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()

    value = (int(data["result"])/ETHER_VALUE)
    return value



def get_transaction(address):

#transaction normal entre un pf a un autre pf 

    transaction_url = api_en_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="desc")
    response = get(transaction_url)
    data = response.json()["result"]

#transaction interne entre un pf et un contrat
    internal_transaction_url = api_en_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="desc")
    response2 = get(internal_transaction_url)
    data2 = response2.json()["result"]


    data.extend(data2)
    data.sort(key=lambda x: int(x["timeStamp"]))
 

    balance_actuel = 0
    balances = []
    times = []



    for transaction in data:
        to = transaction["to"]
        from_addr = transaction["from"]
        value = (int(transaction["value"])/ETHER_VALUE)
        if "gasPrice" in transaction:
            gas = int(transaction["gasUsed"]) * int(transaction["gasPrice"])/ETHER_VALUE
        else:
            gas = int(transaction["gasUsed"]) / ETHER_VALUE
        time = datetime.fromtimestamp(int(transaction["timeStamp"]))

        argent_entrant = to.lower() == address.lower()

        if argent_entrant:
            balance_actuel += value
        else:
            balance_actuel -= value + gas
        balances.append(balance_actuel)
        times.append(time)
    print(balance_actuel)


get_transaction(address)