import requests
from matplotlib import pyplot as plt
from datetime import datetime

API_KEY = "CUUXI6S5B5HETZPC29XJ4SEUCYD4ZH7E6I"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url

def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = requests.get(balance_url)
    data = response.json()

    value = int(data["result"]) / ETHER_VALUE
    return value

def get_transactions(address):
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response = requests.get(transactions_url)
    data = response.json()["result"]

    current_balance = 0
    balances = []
    times = []

    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE

        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            # Vérifie si le solde devient négatif après la transaction
            if current_balance < (value + gas):
                print(f"Transaction suspecte: solde négatif après la transaction à {time}")
                # Vous pouvez choisir de ne pas ajouter cette transaction aux données
            else:
                current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    plt.plot(times, balances, label="Solde (ETH)")
    
    plt.axhline(y=current_balance, color='r', linestyle='--', label='Solde actuel (ETH)')

    # Convertir le solde en dollars
    eth_usd_url = f"{COINGECKO_URL}?ids=ethereum&vs_currencies=usd"
    response2 = requests.get(eth_usd_url)
    data2 = response2.json()
    eth_usd = data2["ethereum"]["usd"]

    usd_balance = current_balance * float(eth_usd)

    plt.xlabel('Time')
    plt.ylabel('Solde (ETH)')
    plt.title('Solde du compte Ethereum au fil du temps')
    plt.text(times[0], max(balances), f"1 ETH = ${eth_usd:.2f}", fontsize=10, color='green', verticalalignment='top', horizontalalignment='left')
    plt.annotate(f'Solde actuel: {current_balance:.2f} ETH (${usd_balance:.2f})', xy=(times[-1], current_balance), xytext=(-50, 30), textcoords='offset points', fontsize=10, color='black', bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='none'), arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color='black'))

    plt.legend()

    # Affichage du prix actuel de l'Ethereum à gauche du graphique
    

    # Annotation pour afficher le solde actuel et le prix de l'ETH

    plt.show()

address = "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
get_transactions(address)
