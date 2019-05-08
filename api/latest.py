from convert import Base

class Latest(Base):
    def __init__(self, base, rate):
        super().__init__()
        self.base = base
        self.custom_list = rates

    def fetch_rates(self):
        if not self.custom_lis:
            if currency == "All":
                rates = self.r.hgetall("rates")
                if rates:
                    return rates
            else:
                self._update_rates()
                return self.r.hgetall("rates")