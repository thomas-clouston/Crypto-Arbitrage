# Imports
import requests


# Lists
prices = []
temp_list = []
found = []


# Setting wager
wager = int(input('Please set your wager: '))

# Retrieving and forming data

# Kucoin
kucoin_request = requests.get('https://api.kucoin.com/api/v1/market/allTickers')
kucoin_request = kucoin_request.json()
data = kucoin_request['data']['ticker']

for index in data:
    trading_pair = index['symbol']
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('-USDT', '')

        # Forming data
        buy_price = index['sell']
        sell_price = index['buy']
        dictionary = {'exchange': 'Kucoin', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# Gate.io
Gateio_request = requests.get('https://api.gateio.ws/api/v4/spot/tickers')
data = Gateio_request.json()

for index in data:
    trading_pair = index['currency_pair']
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('_USDT', '')
        buy_price = index['lowest_ask']
        sell_price = index['highest_bid']
        dictionary = {'exchange': 'Gate.io', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# CoinEx
CoinEx_request = requests.get('https://api.coinex.com/v1/market/ticker/all')
CoinEx_request = CoinEx_request.json()
data = CoinEx_request['data']['ticker']

for index in data:
    trading_pair = index
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('USDT', '')
        buy_price = data[index]['sell']
        sell_price = data[index]['buy']
        dictionary = {'exchange': 'CoinEx', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# Kraken
Kraken_request = requests.get('https://api.kraken.com/0/public/Ticker')
Kraken_request = Kraken_request.json()
data = Kraken_request['result']

for index in data:
    trading_pair = index
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('USDT', '')
        buy_price = data[index]['a'][0]
        sell_price = data[index]['b'][0]
        dictionary = {'exchange': 'Kraken', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# TooBit
TooBit_request = requests.get('https://api.toobit.com/quote/v1/ticker/bookTicker')
data = TooBit_request.json()

for index in data:
    trading_pair = index['s']
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('USDT', '')
        buy_price = index['a']
        sell_price = index['b']
        dictionary = {'exchange': 'TooBit', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# BitMart
BitMart_request = requests.get('https://api-cloud.bitmart.com/spot/quotation/v3/tickers')
BitMart_request = BitMart_request.json()
data = BitMart_request['data']

for index in data:
    trading_pair = index[0]
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('_USDT', '')
        buy_price = index[10]
        sell_price = index[8]
        dictionary = {'exchange': 'BitMart', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# BitGet
BitGet_request = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
BitGet_request = BitGet_request.json()
data = BitGet_request['data']

for index in data:
    trading_pair = index['symbol']
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('USDT', '')
        buy_price = index['askPr']
        sell_price = index['bidPr']
        dictionary = {'exchange': 'BitGet', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# WhiteBit
WhiteBit_request = requests.get('https://whitebit.com/api/v1/public/tickers')
WhiteBit_request = WhiteBit_request.json()
data = WhiteBit_request['result']

for index in data:
    trading_pair = index
    if trading_pair.endswith('USDT'):
        coin = trading_pair.replace('_USDT', '')
        buy_price = data[index]['ticker']['ask']
        sell_price = data[index]['ticker']['bid']
        dictionary = {'exchange': 'WhiteBit', 'coin': coin, 'priceBuy': buy_price, 'priceSell': sell_price}
        prices.append(dictionary)


# Finding arbitrage
for iteration1 in prices:
    buy_exchange = iteration1['exchange']
    coin = iteration1['coin']
    passCount = 0
    if coin in found:
        continue

    if iteration1['priceBuy'] is not None:
        if iteration1['priceBuy'] != '':
            buy_price = float(iteration1['priceBuy'])

            for iteration2 in prices:
                sell_exchange = iteration2['exchange']

                if buy_exchange != sell_exchange:
                    coin2 = iteration2['coin']

                    if iteration2['priceSell'] is not None:
                        if iteration2['priceSell'] != '':
                            sell_price = float(iteration2['priceSell'])

                            if coin == coin2:
                                # Calculating profit
                                if buy_price != sell_price and buy_price != 0 and sell_price != 0:
                                    profit = ((wager / buy_price) * sell_price) - wager
                                    if profit > 0.1 * wager and profit < 0.5 * wager:

                                        # Checking if withdrawal and deposit is enabled
                                        if buy_exchange == 'Kucoin':
                                            Kucoin_check = requests.get(f'https://api.kucoin.com/api/v3/currencies/{coin}')
                                            Kucoin_check = Kucoin_check.json()
                                            data = Kucoin_check['data']['chains'][0]

                                            withdraw_check = data['isWithdrawEnabled']
                                            if withdraw_check is True:
                                                passCount += 1

                                        if sell_exchange == 'Kucoin':
                                            Kucoin_check = requests.get(f'https://api.kucoin.com/api/v3/currencies/{coin}')
                                            Kucoin_check = Kucoin_check.json()
                                            data = Kucoin_check['data']['chains'][0]

                                            deposit_check = data['isDepositEnabled']
                                            if deposit_check is True:
                                                passCount += 1


                                        if buy_exchange == 'Kraken':
                                            Kraken_check = requests.get(f'https://api.kraken.com/0/public/Assets?asset={coin}')
                                            Kraken_check = Kraken_check.json()
                                            data = Kraken_check['result'][coin]

                                            check = data['status']

                                            if check == 'enabled':
                                                passCount += 1
                                            elif check == 'withdrawal_only':
                                                passCount += 1

                                        if sell_exchange == 'Kraken':
                                            Kraken_check = requests.get(f'https://api.kraken.com/0/public/Assets?asset={coin}')
                                            Kraken_check = Kraken_check.json()
                                            data = Kraken_check['result'][coin]

                                            check = data['status']

                                            if check == 'enabled':
                                                passCount += 1
                                            elif check == 'deposit_only':
                                                passCount += 1


                                        if buy_exchange == 'BitMart':
                                            BitMart_check = requests.get(f'https://api-cloud.bitmart.com/spot/v1/currencies')
                                            BitMart_check = BitMart_check.json()
                                            data = BitMart_check['data']['currencies']

                                            for search in data:
                                                searchCoin = search['id']
                                                if searchCoin == coin:
                                                    withdraw_check = search['withdraw_enabled']

                                            if withdraw_check is True:
                                                passCount += 1

                                        if sell_exchange == 'BitMart':
                                            BitMart_check = requests.get(f'https://api-cloud.bitmart.com/spot/v1/currencies')
                                            BitMart_check = BitMart_check.json()
                                            data = BitMart_check['data']['currencies']

                                            for search in data:
                                                searchCoin = search['id']
                                                if searchCoin == coin:
                                                    deposit_check = search['deposit_enabled']

                                            if deposit_check is True:
                                                passCount += 1


                                        if buy_exchange == 'Gate.io':
                                            Gateio_check = requests.get(f'https://api.gateio.ws/api/v4/spot/currencies/{coin}')
                                            data = Gateio_check.json()

                                            withdraw_check = data['withdraw_disabled']
                                            if withdraw_check is False:
                                                passCount += 1

                                        if sell_exchange == 'Gate.io':
                                            Gateio_check = requests.get(f'https://api.gateio.ws/api/v4/spot/currencies/{coin}')
                                            data = Gateio_check.json()

                                            deposit_check = data['deposit_disabled']
                                            if deposit_check is False:
                                                passCount += 1


                                        if buy_exchange == 'CoinEx':
                                            CoinEx_check = requests.get(f'https://api.coinex.com/v1/common/asset/config?coin_type={coin}')
                                            CoinEx_check = CoinEx_check.json()
                                            data = CoinEx_check['data']

                                            for iteration in data:
                                                withdraw_check = data[iteration]['can_withdraw']
                                                if withdraw_check is True:
                                                    passCount += 1
                                                break

                                        if sell_exchange == 'CoinEx':
                                            CoinEx_check = requests.get(f'https://api.coinex.com/v1/common/asset/config?coin_type={coin}')
                                            CoinEx_check = CoinEx_check.json()
                                            data = CoinEx_check['data']

                                            for iteration in data:
                                                deposit_check = data[iteration]['can_deposit']
                                                if deposit_check is True:
                                                    passCount += 1
                                                break


                                        if buy_exchange == 'TooBit':
                                            TooBit_check = requests.get('https://api.toobit.com/api/v1/exchangeInfo')
                                            TooBit_check = TooBit_check.json()
                                            data = TooBit_check['coins']

                                            for search in data:
                                                searchCoin = search['coinId']
                                                if searchCoin == coin:
                                                    withdraw_check = search['allowWithdraw']

                                                    if withdraw_check is True:
                                                        passCount += 1

                                        if sell_exchange == 'TooBit':
                                            TooBit_check = requests.get('https://api.toobit.com/api/v1/exchangeInfo')
                                            TooBit_check = TooBit_check.json()
                                            data = TooBit_check['coins']

                                            for search in data:
                                                searchCoin = search['coinId']
                                                if searchCoin == coin:
                                                    deposit_check = search['allowDeposit']

                                                    if deposit_check is True:
                                                        passCount += 1


                                        if buy_exchange == 'BitGet':
                                            BitGet_check = requests.get(
                                                'https://api.bitget.com/api/v2/spot/public/coins')
                                            BitGet_check = BitGet_check.json()
                                            data = BitGet_check['data']

                                            for search in data:
                                                searchCoin = search['coin']
                                                if searchCoin == coin:
                                                    withdraw_check = search['chains'][0]['withdrawable']

                                                    if withdraw_check == 'true':
                                                        passCount += 1

                                        if sell_exchange == 'BitGet':
                                            BitGet_check = requests.get(
                                                'https://api.bitget.com/api/v2/spot/public/coins')
                                            BitGet_check = BitGet_check.json()
                                            data = BitGet_check['data']

                                            for search in data:
                                                searchCoin = search['coin']
                                                if searchCoin == coin:
                                                    deposit_check = search['chains'][0]['rechargeable']

                                                    if deposit_check == 'true':
                                                        passCount += 1


                                        if buy_exchange == 'WhiteBit':
                                            WhiteBit_check = requests.get('https://whitebit.com/api/v4/public/assets')
                                            data = WhiteBit_check.json()

                                            for search in data:
                                                searchCoin = search
                                                if searchCoin == coin:
                                                    withdraw_check = data[search]['can_withdraw']

                                                    if withdraw_check is True:
                                                        passCount += 1

                                        if sell_exchange == 'WhiteBit':
                                            WhiteBit_check = requests.get('https://whitebit.com/api/v4/public/assets')
                                            data = WhiteBit_check.json()

                                            for search in data:
                                                searchCoin = search
                                                if searchCoin == coin:
                                                    deposit_check = data[search]['can_deposit']

                                                    if deposit_check is True:
                                                        passCount += 1

                                        # Returning opportunities
                                        if passCount >= 2:
                                            print('Coin:', coin, '\n', 'Buy exchange:', buy_exchange, '\n',
                                                  'Buy price:', buy_price, '\n',
                                                  'Sell exchange:', sell_exchange, '\n', 'Sell price:', sell_price,
                                                  '\n', 'Profit:', profit,
                                                  '\n')
                                            found.append(coin)
                                        passCount = 0
