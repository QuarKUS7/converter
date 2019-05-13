from .latest import Latest

class History(Latest):

    def __init__(self, date):
        self.date = str(date)
        self.base = 'CZK'

    def fetch_hist_rates(self):
        self._CNB_URL = self._CNB_URL + f'?date={self.format_date(self.date)}'
        return self._update_rates()

    def format_date(self, date):
        yyyy, mm, dd = str(date).split("-")
        return f"{dd}.{mm}.{yyyy}"

    def _update_rates(self):
        """Parse and insert new rates to db"""
        resp = self._request()
        rates_dict = self._parse_cnb(resp)
        return {"base": self.base, "rates": self._rebase(rates_dict, 1), "date": self.date}