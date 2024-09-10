import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "account",
            "label": _("Account"),
            "fieldtype": "Link",
            "options": "Account",
            "width": 300
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
        }
    ]

def get_data(filters):
    data = []
    accounts = frappe.get_all("Account", fields=["name", "parent_account", "lft", "rgt"])
    
    for account in accounts:
        account_data = get_account_data(account.name, filters)
        for currency, amounts in account_data.items():
            data.append({
                "account": account.name,
                "currency": currency,
                "debit": amounts["debit"],
                "credit": amounts["credit"],
                "balance": amounts["debit"] - amounts["credit"]
            })
    
    return data

def get_account_data(account, filters):
    data = {}
    gl_entries = frappe.get_all(
        "GL Entry",
        filters={
            "account": account,
            "posting_date": ["between", [filters.get("from_date"), filters.get("to_date")]]
        },
        fields=["account_currency", "debit", "credit"]
    )
    
    for entry in gl_entries:
        currency = entry.account_currency
        if currency not in data:
            data[currency] = {"debit": 0, "credit": 0}
        data[currency]["debit"] += entry.debit
        data[currency]["credit"] += entry.credit
    
    return data
