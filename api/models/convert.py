from .base import Base


class Convert(Base):
    def __init__(self, from_curren, amount, to_curren):
        super().__init__()
        self.from_curren = self._check_currency_symbol(from_curren)
        self.amount = amount
        self.to_curren = self._check_currency_symbol(to_curren)

    def convert(self):
        """Function for tringering conversion on initialized Convert object"""
        if not self.from_curren:
            return (
                {"Error": {"input_currency": ["Unknown input currency or symbol."]}},
                400,
            )
        self.from_curren = self._get_rate(self.from_curren)
        if not self.to_curren:
            return (
                {"Error": {"output_currency": ["Unknown output currency or symbol."]}},
                400,
            )
        self.to_curren = self._get_rate(self.to_curren)
        out = {
            "input": {
                "amount": self.amount,
                "currency": next(iter(self.from_curren.keys())),
            },
            "output": {},
        }
        for key, value in self.to_curren.items():
            out["output"][key] = self._change(float(value))
        return out

    def _change(self, currency):
        # Formula for currency change
        return (
            float(next(iter(self.from_curren.values())))
            * float(self.amount)
            / float(currency)
        )
