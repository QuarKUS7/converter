from .latest import Latest
from utils import format_to_dot_date


class History(Latest):
    def __init__(self, base, rates, date):
        super().__init__(base, rates)
        self.date = str(date)

    def fetch_hist_rates(self):
        self._CNB_URL = self._CNB_URL + f'?date={format_to_dot_date(self.date)}'
        resp = self._request()
        rates_dict = self._parse_cnb(resp)
        return {"base": self.base, "rates": self._rebase(rates_dict, self.base_rate), "date": self.date}