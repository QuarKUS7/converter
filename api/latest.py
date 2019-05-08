from convert import Base

class Latest(Base):
    def __init__(self, base, rates):
        super().__init__()
        self.base = self._check_currency_symbol(base)
        self.custom_list = rates

    def fetch_rates(self):
        rates = self._get_or_update()
        if self.custom_list:
            rates = {key:value for (key, value) in rates.items() if key in self.custom_list}
        if self.base:
            return self._rebase(rates)
        return rates

    def _rebase(self, dict_rates):
        base_rate = dict_rates[self.base]
        return dict((k, float(v)/float(base_rate)) for k, v in dict_rates.items())