from urllib.request import urlopen


def exchange(currency_from, currency_to, amount_from):
    """
    This function is designed for calculating currency
    There are three variables you are required to enter,
    respectively currency of two kinds of money, and the
    amount of the money.
    For example, If you want to calculate how much is 90 dollars
    in Chinese Yuan, you should enter: 'USD', 'CNY', 90
    the former is the money you want to convert from,
    and the latter one is the currency you want to convert to
    the last variable is the amount of the former money.
    The Amount is a float, note that.
    """
    currency_from = currency_from.upper()
    currency_to = currency_to.upper()
    website = 'http://cs1110.cs.cornell.edu/2016fa/a1server.php?'
    msg = urlopen('%sfrom=%s&to=%s&amt=%s' % (website, currency_from, currency_to, str(amount_from)))
    msgstr = msg.read()
    msg.close()
    psg = msgstr.decode('ascii')
    analyse = psg.split(',')[0:2]
    former = analyse[0].split(': ')[1]
    latter = analyse[1].split(': ')[1]
    result = eval(latter)
    return result


def test_exchange():
    assert(exchange('USD', 'CNY', 90))


def test_all():
    test_exchange()
    help(exchange)
    print("All tests passed")


def main():
    cur_from = input('Please enter the currency you want to convert from:\n')
    cur_to = input('Please enter the currency you want to convert to:\n')
    amt = input('Please enter the amount of the currency you want to convert from:\n')
    print(exchange(cur_from, cur_to, amt))


if __name__ == '__main__':
    main()

