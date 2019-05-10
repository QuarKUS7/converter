from convert import Base

class Latest(Base):
    def __init__(self, base, rates):
        super().__init__()
        self.base = self._check_currency_symbol(base)
        self.custom_list = [self._check_currency_symbol(rate) for rate in rates]

    def fetch_rates(self):
        if not self.base:
            return (
                {"Error": {"base": ["Unknown base currency or symbol."]}},
                400,
            )
        if None in self.custom_list:
            return (
                {"Error": {"rates": ["Unknown rate currency or symbol."]}},
                400,
            )
        rates = self._get_or_update()
        if "All" not in self.custom_list:
            rates = {k:v for (k, v) in rates.items() if k in self.custom_list}
        return {"base": self.base, "rates":self._rebase(rates)}

    def _rebase(self, dict_rates):
        base_rate = next(iter(self._get_rate(self.base).values()))
        return {k:1 / v * float(base_rate) for k, v in dict_rates.items()}