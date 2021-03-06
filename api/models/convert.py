from .base import Base
import datetime
from utils import format_from_dot_date, format_to_dot_date, cnb_day


class Convert(Base):
    def __init__(self, from_curren, amount, to_curren):
        super().__init__()
        self.from_curren = self._check_currency_symbol(from_curren)
        self.amount = amount
        self.to_curren = self._check_currency_symbol(to_curren)

    def convert(self, date):
        """Function for tringering conversion on initialized Convert object"""
        if not date:
            date = format_to_dot_date(cnb_day())
            # Store input date
            input_date = date
        elif date:
            # Store input date
            input_date = format_to_dot_date(date)
            date = format_to_dot_date(cnb_day(date))
        if not self.from_curren:
            return (
                {"Error": {"input_currency": ["Unknown input currency or symbol."]}},
                400,
            )
        self.from_curren, _ = self._get_rate(self.from_curren, date)
        if not self.to_curren:
            return (
                {"Error": {"output_currency": ["Unknown output currency or symbol."]}},
                400,
            )
        self.to_curren, date = self._get_rate(self.to_curren, date)
        out = {
            "input": {
                "date": format_from_dot_date(input_date),
                "amount": self.amount,
                "currency": next(iter(self.from_curren.keys()))
            },
            "output": {"effective date": format_from_dot_date(date)},

        }
        for key, value in self.to_curren.items():
            if not value:
                continue
            out["output"][key] = self._change(float(value))
        return out

    def _change(self, currency):
        # Formula for currency change
        return (
            float(next(iter(self.from_curren.values())))
            * float(self.amount)
            / float(currency)
        )
