"""Currency formatting. TODO(Builder): card "Multi-currency invoices"."""

SYMBOLS = {"USD": "$"}


def format_amount(amount, currency="USD"):
    return f"{SYMBOLS.get(currency, '$')}{amount:,.2f}"
