from historicalData import show_history


def bitcoin():
    return show_history("bitcoin")


def litecoin():
    return show_history('litecoin')


def xrp():
    return show_history('xrp')


def ethereum():
    return show_history('ethereum')


def syscoin():
    return show_history('syscoin')


def cardano():
    return show_history('cardano')


def tron():
    return show_history('tron')


def vechain():
    return show_history('vechain')


def electroneum():
    return show_history('electroneum')


def show(curre):
    return globals()[curre]()
# print(show('bitcoin'))
