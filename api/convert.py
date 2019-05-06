import requests
import datetime
import redis
import json


class Convert():

    _CNB_URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"

    r = redis.Redis(host='redis', decode_responses=True)

    def __init__(self, from_curren, amount, to_curren):
        self._symbol_list = self._load_symbols()
        self.from_curren = self._check_currency_symbol(from_curren)
        self.amount = amount
        self.to_curren = self._check_currency_symbol(to_curren)

    def _load_symbols(self):
        # Load symbol list
        with open('symbols.json', 'r', encoding='utf-8') as f:
            symbol_list = json.load(f)
        return list(symbol_list.values())

    def _check_currency_symbol(self, curren):
        """Check if symbol in symbol list. Returns code of the currency"""
        if curren == 'All':
            return 'All'
        return next((item['code'] for item in self._symbol_list if curren.upper() in [item['symbol'], item['code']]), None)
            
    def convert(self):
        """Function for tringering conversion on initialized Convert object"""
        if not self.from_curren:
            return {"Error":{"input_currency":["Unknown input currency or symbol."]}}, 400
        self.from_curren = self._get_rate(self.from_curren)
        if not self.to_curren:
            return {"Error":{"output_currency":["Unknown output currency or symbol."]}}, 400
        self.to_curren = self._get_rate(self.to_curren)
        out = {"input": {"amount": self.amount, "currency": next(iter(self.from_curren.keys()))}, "output": {}}
        for key, value in self.to_curren.items():
            out["output"][key] = self._change(float(value))
        return out

    def _change(self, currency):
        # Formula for currency chnage
        return float(next(iter(self.from_curren.values()))) * float(self.amount) / float(currency)
        
    def _request(self):
        """Request txt from CNB"""
        response = requests.get(self._CNB_URL)
        if response.content:
            return response.text

    def _get_rate(self, currency):
        """Return rates from db or trigers update for rates"""
        # All is for missing output currency
        if currency == 'All':
            rates = self.r.hgetall('rates')
            if rates:
                return rates
            else:
                self._update_rates()
                return self.r.hgetall('rates')
        rate = self.r.hget('rates', currency)
        if rate:
            return {currency:rate}
        else:
            self._update_rates()
            return {currency: self.r.hget('rates', currency)}

    def _update_rates(self):
        """Parse and insert new rates to db"""
        resp = self._request()
        rates_dict = self._parse_cnb(resp)
        self._insert_into_redis(rates_dict)

    def _parse_cnb(self, text):
        """Returns dict of currency and rate from CNB rates"""
        rates_dict = {}
        breakpoint()
        for row in text.split('\n')[2:-1]:
            rates_dict[row.split('|')[-2]] = float(row.split('|')[-1].replace(',','.')) / float(row.split('|')[-3].replace(',','.'))
        # CZK not in the list so added manually
        rates_dict['CZK'] = '1'
        return rates_dict
    
    def _insert_into_redis(self,to_insert):
        self.r.hmset('rates', to_insert)
        self.r.expire('rates', datetime.timedelta(minutes=1))


if __name__ == '__main__':
    import redis
    r = redis.Redis(host='127.0.0.1',port='6379', decode_responses=True)
    cnvrt = Convert('MXN', 11.1, 'All')
    print(cnvrt.convert())