import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "account_group", "label": _("Account Group"), "fieldtype": "Data", "width": 150},
        {"fieldname": "account_name", "label": _("Account Name"), "fieldtype": "Data", "width": 250},
        {"fieldname": "currency", "label": _("Currency"), "fieldtype": "Data", "width": 100},
        {"fieldname": "total_amount", "label": _("Total Amount"), "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("date_range"):
        conditions += " AND posting_date BETWEEN %(from_date)s AND %(to_date)s"
    if filters.get("account_group"):
        conditions += " AND parent = %(account_group)s"
    if filters.get("currency"):
        conditions += " AND account_currency = %(currency)s"

    accounts = frappe.db.sql("""
        SELECT 
            parent as account_group, 
            name as account_name, 
            account_currency as currency, 
            sum(debit - credit) as total_amount
        FROM 
            `tabGL Entry`
        WHERE 
            company = %(company)s
            {conditions}
        GROUP BY 
            parent, account_currency
        ORDER BY 
            parent ASC
    """.format(conditions=conditions), filters, as_dict=True)

    data = []
    for account in accounts:
        data.append({
            "account_group": account.account_group,
            "account_name": account.account_name,
            "currency": account.currency,
            "total_amount": account.total_amount
        })

    return data
