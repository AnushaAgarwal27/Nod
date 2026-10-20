"""InvoiceFlow: invoicing for freelancers. The demo app the Builder agent edits."""
from flask import Flask, jsonify, render_template_string, request

from currency import format_amount
from reminders import due_reminders

app = Flask(__name__)

INVOICES = [
    {"id": 1, "client": "Acme Studio", "email": "billing@acme.example", "amount": 1200, "currency": "USD", "days_overdue": 9, "paid": False},
    {"id": 2, "client": "Lumen Weddings", "email": "hello@lumen.example", "amount": 3400, "currency": "USD", "days_overdue": 0, "paid": False},
    {"id": 3, "client": "Northwind", "email": "ap@northwind.example", "amount": 800, "currency": "USD", "days_overdue": 21, "paid": False},
]


# render_template_string autoescapes every {{ }} value, so client input can't inject HTML.
INDEX_HTML = """<h1>InvoiceFlow</h1>
<table border=1 cellpadding=6>
{% for i in invoices %}
  <tr><td>{{ i.id }}</td><td>{{ i.client }}</td><td>{{ format_amount(i.amount, i.currency) }}</td>
  <td>{% if i.paid %}paid{% else %}{{ i.days_overdue }} days overdue{% endif %}</td></tr>
{% endfor %}
</table>"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML, invoices=INVOICES, format_amount=format_amount)


@app.get("/api/invoices")
def list_invoices():
    return jsonify(INVOICES)


@app.post("/api/invoices")
def create_invoice():
    data = request.get_json(force=True)
    invoice = {
        "id": len(INVOICES) + 1,
        "client": data["client"],
        "email": data.get("email", ""),
        "amount": float(data["amount"]),
        "currency": data.get("currency", "USD"),
        "days_overdue": 0,
        "paid": False,
    }
    INVOICES.append(invoice)
    return jsonify(invoice), 201


@app.get("/api/reminders")
def reminders():
    return jsonify(due_reminders(INVOICES))


if __name__ == "__main__":
    app.run(port=5050, debug=False)
