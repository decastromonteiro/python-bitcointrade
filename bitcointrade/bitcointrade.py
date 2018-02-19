# coding=utf-8
import requests
import datetime


class BitcoinTradePublic:
    def __init__(self, version='v1', coin='BTC'):
        self.url = 'https://api.bitcointrade.com.br/{version}/public/{coin}/{method}/'
        self.version = version
        self.coin = coin

    def get_ticker(self, method='ticker'):
        """https://api.bitcointrade.com.br/v1/public/BTC/ticker"""
        response = requests.get(self.url.format(version=self.version, coin=self.coin, method=method))

        response.close()
        return response.json()

    def get_orders(self, method='orders', order_by='unit_price'):
        """https://api.bitcointrade.com.br/v1/public/BTC/orders"""
        response = requests.get(self.url.format(version=self.version, coin=self.coin, method=method))

        orders_dict = response.json()
        if orders_dict.get('data'):
            orders_list = orders_dict.get('data').get('bids')
            ordered_orders_list = sorted(orders_list, key=lambda k: k[order_by])
            response.close()
            return {'message': orders_dict.get('message'), 'data': ordered_orders_list}
        response.close()
        return response.json()

    def get_trades(self,
                   method='trades?start_time={start_time}&end_time={end_time}&page_size={page_size}&current_page=1',
                   start_time=(datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
                   end_time=datetime.datetime.now().isoformat(),
                   page_size=100):
        """https://api.bitcointrade.com.br/v1/public/BTC/trades?
        start_time=2016-10-01T00:00:00-03:00&end_time=2018-10-10T23:59:59-03:00&page_size=100&current_page=1"""
        response = requests.get(self.url.format(version=self.version, coin=self.coin,
                                                method=method.format(start_time=start_time,
                                                                     end_time=end_time,
                                                                     page_size=page_size)))
        response.close()
        return response.json()


class BitcoinTradeBitcoin:
    def __init__(self, api_token, version='v1', coin='BTC'):
        super().__init__()
        self.url = 'https://api.bitcointrade.com.br/{version}/bitcoin/{method}'
        self.api_token = api_token
        self.version = version
        self.coin = coin

    def get_withdraw_fee(self, method='withdraw/fee'):
        """https://api.bitcointrade.com.br/v1/bitcoin/withdraw/fee"""

        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(self.url.format(version=self.version, method=method), headers=auth_header)

        return response.json()

    def get_withdraw_list(self,
                          method='withdraw?page_size={page_size}&current_page=1&'
                                 'status={status}&start_date={start_date}&end_date={end_date}',
                          page_size=100, status='pending',
                          start_date=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                          end_date=datetime.datetime.now().strftime('%Y-%m-%d')):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(self.url.format(version=self.version,
                                                method=method.format(page_size=page_size,
                                                                     status=status,
                                                                     start_date=start_date,
                                                                     end_date=end_date)),
                                headers=auth_header)

        return response.json()

    def get_deposit_list(self,
                         method='deposits?page_size={page_size}&current_page=1&'
                                'status={status}&start_date={start_date}&end_date={end_date}',
                         page_size=100, status='confirmed',
                         start_date=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                         end_date=datetime.datetime.now().strftime('%Y-%m-%d')):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(self.url.format(version=self.version,
                                                method=method.format(page_size=page_size,
                                                                     status=status,
                                                                     start_date=start_date,
                                                                     end_date=end_date)),
                                headers=auth_header)

        return response.json()

    def create_withdraw(self, destination: str, amount: float, fee: str, fee_type: str, method='withdraw'):
        """ {
         "destination": "1AU4BoYaxSunFtraWikEMYXJ41c9bvQG6Wa2",
         "amount": 0.06,
         "fee": 0.0005037,
         "fee_type": "slow"
         }
        """

        data_dict = {
            'destination': str(destination),
            'amount': float(amount),
            'fee': float(fee),
            'fee_type': str(fee_type)
        }

        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.post(url=self.url.format(version=self.version, method=method),
                                 json=data_dict, headers=auth_header)

        return response.json()


class BitcoinTradeMarket:
    def __init__(self, api_token, version='v1', coin='BTC'):
        super().__init__()
        self.url = 'https://api.bitcointrade.com.br/{version}/market{method}'
        self.api_token = api_token
        self.version = version
        self.coin = coin

    def get_book_orders(self, method='?currency={coin}'):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(self.url.format(version=self.version, method=method.format(coin=self.coin)),
                                headers=auth_header)

        return response.json()

    def get_summary(self, method='/summary?currency={coin}'):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(self.url.format(version=self.version, method=method.format(coin=self.coin)),
                                headers=auth_header)

        return response.json()

    def get_users_orders(self,
                         method='/user_orders/list?status={status}&start_date={start_date}&'
                                'end_date={end_date}&currency={coin}&type={type}&page_size={page_size}&current_page=1',
                         status='executed_completely', page_size=100, _type='buy',
                         start_date=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                         end_date=datetime.datetime.now().strftime('%Y-%m-%d')):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(self.url.format(version=self.version,
                                                method=method.format(
                                                    coin=self.coin, status=status, page_size=page_size, _type=_type,
                                                    start_date=start_date, end_date=end_date
                                                )), headers=auth_header)

        return response.json()

    def get_estimated_price(self, method='/estimated_price?amount={amount}&currency={coin}&type={_type}',
                            amount=0, _type='buy'):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(
            self.url.format(version=self.version, method=method.format(amount=amount, _type=_type, coin=self.coin),
                            headers=auth_header))

        return response.json()

    def create_order(self, amount: float, _type: str, unit_price: int, subtype='market', method='/create_order'):
        """
                {
          "currency":"BTC",
          "amount": 0.5,
          "type": "buy",
          "subtype": "market",
          "unit_price": 1000
        }
        """
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        data_dict = {
            'currency': self.coin,
            'amount': float(amount),
            'type': str(_type),
            'subtype': str(subtype),
            'unit_price': int(unit_price)
        }

        response = requests.post(url=self.url.format(version=self.version, method=method),
                                 json=data_dict,
                                 headers=auth_header)

        return response.json()

    def delete_order(self, method='/user_orders/', order_id=None):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        data_dict = {'id': order_id}

        response = requests.delete(url=self.url.format(version=self.version, method=method), headers=auth_header,
                                   data=data_dict)

        return response.json()


class BitcoinTradeWallets:
    def __init__(self, api_token, version='v1'):
        self.url = "https://api.bitcointrade.com.br/{version}/wallets/{method}"
        self.api_token = api_token
        self.version = version

    def get_balance(self, method='balance'):
        auth_header = {'Authorization': 'ApiToken {api_token}'.format(api_token=self.api_token)}

        response = requests.get(
            self.url.format(version=self.version, method=method), headers=auth_header)

        return response.json()
