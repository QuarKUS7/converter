import requests
import datetime
import redis

class Convert():

    _CNB_URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"

    r = redis.Redis(host='redis', decode_responses=True)

    def __init__(self, from_curren, amount, to_curren=None):
        self.from_curren = self._get_rate(from_curren)
        self.amount = amount
        self.to_curren = self._get_rate(to_curren)

    def convert(self):
        out = {"input": {"amount": self.amount, "currency": next(iter(self.from_curren.keys()))}, "output": {}}
        for key, value in self.to_curren.items():
            out["output"][key] = self._change(float(value))
        return out

    def _change(self, currency):
        return float(next(iter(self.from_curren.values()))) * float(self.amount) / float(currency)
        
    def _request(self):
        try:
            response = requests.get(self._CNB_URL)
        except:
            return {'Error': 'something went wronge try again later'}

        if response.content:
            return response.text

    def _get_rate(self, currency):
        if currency:
            rate = self.r.hget('rates', currency)
            if rate:
                return {currency:rate}
            else:
                self._update_rates()
                return {currency: self.r.hget('rates', currency)}
        rates = self.r.hgetall('rates')
        if rates:
            return rates
        else:
            self._update_rates()
            return self.r.hgetall('rates')

    def _update_rates(self):
        print('updated')
        resp = self._request()
        rates_dict = self._parse_cnb(resp)
        self._insert_into_redis(rates_dict)


    def _parse_cnb(self, text):
        rates_dict = {}
        for row in text.split('\n')[2:-1]:
            rates_dict[row.split('|')[-2]] = row.split('|')[-1].replace(',','.')
        return rates_dict
    
    def _insert_into_redis(self,to_insert):
        self.r.hmset('rates', to_insert)
        self.r.expire('rates', datetime.timedelta(minutes=1))


if __name__ == '__main__':
    import redis
    r = redis.Redis(host='127.0.0.1',port='6379', decode_responses=True)
    cnvrt = Convert(r, 'RUB', 11.1)
    print(cnvrt.convert())