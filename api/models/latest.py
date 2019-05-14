from .base import Base
import datetime
from utils import format_to_dot_date


class Rates(Base):
    def __init__(self, base, rates):
        super().__init__()
        self.base = self._check_currency_symbol(base)
        #self.date = format_to_dot_date(datetime.datetime.today().strftime('%Y-%m-%d'))
        self.custom_list = [self._check_currency_symbol(rate) for rate in rates]
        #self.base_rate = next(iter(self._get_rate(self.base, self.date).values()))

    def fetch_rates(self, date):
        base_rate = next(iter(self._get_rate(self.base, date).values()))
        if not self.base:
            return ({"Error": {"base": ["Unknown base currency or symbol."]}}, 400)
        if None in self.custom_list:
            return ({"Error": {"rates": ["Unknown rate currency or symbol."]}}, 400)
        rates = self._get_or_update(date)
        if "All" not in self.custom_list:
            # filtering custom rates
            rates = {k: v for (k, v) in rates.items() if k in self.custom_list}
        return {"base": self.base, "rates": self._rebase(rates, base_rate)}

    def _rebase(self, dict_rates, base_rate):
        """Function for rebasing rates in dict"""
        #base_rate = next(iter(self._get_rate(self.base).values()))
        return {k: 1 / float(v) * float(base_rate) for k, v in dict_rates.items()}
