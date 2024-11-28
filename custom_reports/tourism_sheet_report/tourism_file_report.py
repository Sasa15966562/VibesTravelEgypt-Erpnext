from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    # Handle both dictionary-style filters and object-style filters
    sales_order = filters.get("sales_order") if isinstance(filters, dict) else getattr(filters, "sales_order", None)
    item_code = filters.get("item_code") if isinstance(filters, dict) else getattr(filters, "item_code", None)
    
    if not sales_order:
        frappe.throw(_("Please select a Tourism File"))
        
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "expense_category",
            "label": _("Expenses"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "rate",
            "label": _("Rate"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "egp",
            "label": _("EGP"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "usd",
            "label": _("USD"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "eur",
            "label": _("EUR"),
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    # Handle both dictionary-style filters and object-style filters
    sales_order = filters.get("sales_order") if isinstance(filters, dict) else getattr(filters, "sales_order", None)
    item_code = filters.get("item_code") if isinstance(filters, dict) else getattr(filters, "item_code", None)
    
    data = []
    file_doc = frappe.get_doc("Sales Order", sales_order)
    
    # Get Lead Department from the linked Lead
    lead_department = None
    if file_doc.opportunity:
        opportunity = frappe.get_doc("Opportunity", file_doc.opportunity)
        if opportunity.lead:
            lead = frappe.get_doc("Lead", opportunity.lead)
            lead_department = lead.lead_department
    
    # Initialize totals
    total_cost_egp = 0
    total_cost_usd = 0
    
    # Process items under the Lead Department
    if lead_department:
        data.append({
            "expense_category": lead_department,
            "indent": 0,
            "is_group": 1
        })
        
        department_total_egp = 0
        department_total_usd = 0
        
        # Filter items based on item_code if specified
        items = [item for item in file_doc.items if not item_code or item.item_code == item_code]
        
        for item in items:
            # Handle multicurrency items
            if item.currency == "USD":
                usd_amount = item.amount
                egp_amount = item.amount * item.conversion_rate
            elif item.currency == "EGP":
                egp_amount = item.amount
                usd_amount = item.amount / item.conversion_rate if item.conversion_rate else 0
            else:
                egp_amount = item.amount
                usd_amount = 0
            
            data.append({
                "expense_category": item.item_name,
                "rate": item.conversion_rate,
                "egp": egp_amount,
                "usd": usd_amount,
                "indent": 1
            })
            department_total_egp += egp_amount
            department_total_usd += usd_amount
            
            total_cost_egp += egp_amount
            total_cost_usd += usd_amount
        
        # Add department total
        if department_total_egp > 0 or department_total_usd > 0:
            data.append({
                "expense_category": f"{lead_department} Total",
                "egp": department_total_egp,
                "usd": department_total_usd,
                "indent": 0,
                "is_total_row": 1
            })
    
    # Add Expenses Total
    data.append({
        "expense_category": "Expenses Total",
        "egp": total_cost_egp,
        "usd": total_cost_usd,
        "indent": 0,
        "is_total_row": 1
    })
    
    # Get Revenue from file (adjusted for item filter)
    if item_code:
        revenue_items = [item for item in file_doc.items if item.item_code == item_code]
        revenue_egp = sum(item.amount for item in revenue_items)
        revenue_usd = revenue_egp / file_doc.conversion_rate if file_doc.conversion_rate else 0
    else:
        revenue_egp = file_doc.grand_total
        revenue_usd = revenue_egp / file_doc.conversion_rate if file_doc.conversion_rate else 0
    
    data.append({
        "expense_category": "Revenue",
        "egp": revenue_egp,
        "usd": revenue_usd,
        "indent": 0
    })
    
    # Calculate Profit
    profit_egp = revenue_egp - total_cost_egp
    profit_usd = revenue_usd - total_cost_usd
    
    data.append({
        "expense_category": "Profit",
        "egp": profit_egp,
        "usd": profit_usd,
        "indent": 0,
        "is_total_row": 1
    })
    
    # Calculate Profit Percentage
    if revenue_egp:
        profit_percentage = (profit_egp / revenue_egp) * 100
        data.append({
            "expense_category": "Profit Percentage",
            "egp": f"{profit_percentage:.2f}%",
            "indent": 0
        })
    
    return data

def get_filter_data():
    return [
        {
            "fieldname": "sales_order",
            "label": _("Tourism File"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "reqd": 1
        },
        {
            "fieldname": "item_code",
            "label": _("Sales Order Item"),
            "fieldtype": "Link",
            "options": "Item",
            "get_query": lambda: {
                "query": "frappe.client.get_list",
                "filters": {
                    "parent": "sales_order",
                    "parenttype": "Sales Order",
                    "doctype": "Sales Order Item",
                    "fields": ["item_code"]
                }
            }
        }
    ]
