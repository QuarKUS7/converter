import requests
import datetime
import redis
import json


class Base:

    _CNB_URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"

    r = redis.Redis(host="redis", decode_responses=True)

    def __init__(self):
        self._symbol_list = self._load_symbols()

    def _load_symbols(self):
        # Load symbol list
        with open("symbols.json", "r", encoding="utf-8") as f:
            symbol_list = json.load(f)
        return list(symbol_list.values())

    def _check_currency_symbol(self, curren):
        """Check if symbol in symbol list. Returns code of the currency"""
        if curren == "All":
            return "All"
        if not curren:
            return None
        return next(
            (
                item["code"]
                for item in self._symbol_list
                if curren in [item["symbol"], item["code"]]
            ),
            None,
        )

    def _update_rates(self, date):
        """Parse and insert new rates to db"""
        resp = self._request(date)
        rates_dict, date = self._parse_cnb(resp)
        self._insert_into_redis(rates_dict, date)

    def _parse_cnb(self, text):
        print("parsed")
        """Returns dict of currency and rate from CNB rates"""
        # Parse 10 characters which is the CNB date
        date = text[:10]
        rates_dict = {}
        for row in text.split("\n")[2:-1]:
            rates_dict[row.split("|")[-2]] = float(
                row.split("|")[-1].replace(",", ".")
            ) / float(row.split("|")[-3].replace(",", "."))
        # CZK not in the list so added manually
        rates_dict["CZK"] = "1"
        return rates_dict, date

    def _insert_into_redis(self, to_insert, date):
        self.r.hmset(date, to_insert)

    def _request(self, date):
        """Request txt from CNB"""
        response = requests.get(self._CNB_URL + f"?date={date}")
        if response.content:
            return response.text

    def _get_rate(self, currency, date):
        """Return rates from db or trigers update for rates"""
        # All is for missing option
        if currency == "All":
            rates = self.r.hgetall(date)
            if rates:
                return rates
            else:
                self._update_rates(date)
                return self.r.hgetall(date)
        rate = self.r.hget(date, currency)
        if rate:
            return {currency: rate}
        else:
            self._update_rates(date)
            return {currency: self.r.hget(date, currency)}
