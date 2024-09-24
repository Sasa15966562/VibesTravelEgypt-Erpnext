import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "party",
            "label": _("Party"),
            "fieldtype": "Dynamic Link",
            "options": "party_type",  # Now dynamically linked to party_type
            "width": 200
        },
        {
            "fieldname": "party_type",
            "label": _("Party Type"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "currency",
            "label": _("Currency"),
            "fieldtype": "Link",
            "options": "Currency",
            "width": 100
        },
        {
            "fieldname": "debit",
            "label": _("Debit"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150
        },
        {
            "fieldname": "credit",
            "label": _("Credit"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150
        },
        {
            "fieldname": "balance",
            "label": _("Balance"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150
        },
        {
            "fieldname": "posting_date",
            "label": _("Posting Date"),
            "fieldtype": "Date",
            "width": 120
        }
    ]


def get_data(filters):
    data = []
    
    # Fetching both supplier and customer GL entries
    gl_entries = frappe.get_all(
        "GL Entry",
        filters={
            "party_type": ["in", ["Customer", "Supplier"]],
        },
        fields=["party", "party_type", "account_currency", "debit", "credit", "posting_date"]
    )
    
    # Processing data to include balance calculations
    for entry in gl_entries:
        balance = entry.debit - entry.credit
        data.append({
            "party": entry.party,
            "party_type": entry.party_type,
            "currency": entry.account_currency,
            "debit": entry.debit,
            "credit": entry.credit,
            "balance": balance,
            "posting_date": entry.posting_date
        })
    
    return data
