from .latest import Latest
from utils import format_to_dot_date


class History(Latest):
    def __init__(self, base, rates):
        super().__init__(base, rates)

    def fetch_hist_rates(self, fetch_date):
        form_date = format_to_dot_date(str(fetch_date))
        rates = self._get_or_update(form_date)
        return {form_date: self._rebase(rates, self.base_rate)}
