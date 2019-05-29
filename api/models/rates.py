from .base import Base
import datetime
from utils import format_to_dot_date


class Rates(Base):
    """Class used for fetchig rates for latest and history endpoints"""
    def __init__(self, base, rates):
        super().__init__()
        self.base = self._check_currency_symbol(base)
        self.custom_list = [self._check_currency_symbol(rate) for rate in rates]

    def fetch_rates(self, date):
        # Get base rate
        rates, _ = self._get_rate(self.base, date)
        base_rate = next(iter(rates.values()))
        # Get output rates
        rates, date = self._get_rate("All", date)
        if "All" not in self.custom_list:
            # filtering custom rates if needed
            rates = {k: v for (k, v) in rates.items() if k in self.custom_list}
        return self._rebase(rates, base_rate), date

    def _rebase(self, dict_rates, base_rate):
        """Function for rebasing rates in dict"""
        return {k: 1 / float(v) * float(base_rate) for k, v in dict_rates.items()}
