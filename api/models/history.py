from .latest import Latest
from utils import format_to_dot_date


class History(Latest):
    def __init__(self, base, rates):
        super().__init__(base, rates)

    def fetch_hist_rates(self, fetch_date):
        form_date = format_to_dot_date(str(fetch_date))
        self._CNB_URL = self._CNB_URL + f'?date={form_date}'
        resp = self._request()
        rates_dict = self._parse_cnb(resp)
        return {form_date: self._rebase(rates_dict, self.base_rate)}
