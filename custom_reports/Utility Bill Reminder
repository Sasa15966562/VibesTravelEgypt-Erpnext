import frappe
from frappe.utils import add_days, add_months
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification

def generate_reminder_event(doc, method):
    # Create calendar event
    event = frappe.get_doc({
        "doctype": "Event",
        "subject": f"Payment Reminder: {doc.bill_type} Bill",
        "starts_on": add_days(doc.due_date, -doc.reminder_days_before),
        "event_type": "Private",
        "description": f"Reminder to pay {doc.bill_type} bill\nDue Date: {doc.due_date}\nAmount: {doc.approximate_amount or 'Not specified'}",
        "send_reminder": 1,
        "remind_before": "30 minutes"
    })
    event.insert()
    
    # Create notification for each user
    for user_row in doc.notify_users:
        notification_doc = {
            "type": "Alert",
            "document_type": "Utility Bill Reminder",
            "document_name": doc.name,
            "for_user": user_row.user,
            "subject": f"Payment Reminder: {doc.bill_type} Bill",
            "email_content": f"Please note that the {doc.bill_type} bill payment is due on {doc.due_date}.\nAmount: {doc.approximate_amount or 'Not specified'}"
        }
        enqueue_create_notification(notification_doc)
    
    # Create next reminder if recurring
    if doc.is_recurring:
        next_date = None
        if doc.frequency == "Monthly":
            next_date = add_months(doc.due_date, 1)
        elif doc.frequency == "Quarterly":
            next_date = add_months(doc.due_date, 3)
        elif doc.frequency == "Yearly":
            next_date = add_months(doc.due_date, 12)
            
        if next_date:
            new_reminder = frappe.copy_doc(doc)
            new_reminder.due_date = next_date
            new_reminder.insert()
