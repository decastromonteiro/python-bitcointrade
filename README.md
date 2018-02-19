


python-bitcointrade
======

bitcointrade is a Python Wrapper for BitcoinTrade API

Installation
======

```bash
git clone https://github.com/decastromonteiro/python-bitcointrade.git
cd python-bitcointrade
python setup.py install
```

Basic Usage
======

Below you can see some of the available BitcoinTrade API methods you can use:

```python
import bitcointrade
bt_public = bitcointrade.BitcoinTradePublic()
bt_public.get_ticker()
bt_bitcoin = bitcointrade.BitcoinTradeBitcoin(api_token='api_token')
bt_bitcoin.get_withdraw_fee()
bt_market = bitcointrade.BitcoinTradeMarket(api_token='api_token')
bt_market.create_order(amount=0.5, _type='buy', unit_price=34000)
bt_wallet = bitcointrade.BitcoinTradeWallets(api_tolen='api_token')
bt_wallter.get_balance()
```

References
======
* [BitcoinTrade API Documentation](https://apidocs.bitcointrade.com.br/)


# TODO
Implement unit tests
