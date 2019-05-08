from convert import Base

class Latest(Base):
    def __init__(self, base, rates):
        super().__init__()
        self.base = self._check_currency_symbol(base)
        self.custom_list = rates

    def fetch_rates(self):
        if not self.custom_list and not self.base:
            return self._get_or_update()
        elif self.custom_list and not self.base:
            rates = self._get_or_update()
            return {key:value for (key, value) in rates.items() if key in self.custom_list}
        elif not self.custom_list and self.base:
            return self._rebase(self._get_or_update())
        elif self.custom_list and self.base:
            rates = self._get_or_update()
            return self._rebase({key:value for (key, value) in rates.items() if key in self.custom_list}, self.base)

    def _rebase(self, dict_rates):
        base_rate = dict_rates[self.base]
        return dict((k, float(v)/float(base_rate)) for k, v in dict_rates.items())