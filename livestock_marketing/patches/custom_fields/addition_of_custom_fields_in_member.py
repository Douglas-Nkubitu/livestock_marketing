import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields={
        "Member": [
            {
                "label":"Mobile Number",
                "fieldname":"mobile_number",
                "fieldtype":"Data",
                "insert_after":"membership_type",
                "reqd": 1,
            },
            {
                "label":"Member Details",
                "fieldname":"members_details",
                "insert_after":"image",
                "fieldtype":"Section Break",
            },
            {
                "label":"Member Categories",
                "fieldname":"member_categories",
                "fieldtype":"Select",
                "options": "\nMember\nNon Member",
                "insert_after":"members_details",
                "reqd": 1,
            },
            {
                "label":"Crush Name",
                "fieldname":"crush_name",
                "insert_after":"member_categories",
                "fieldtype":"Link",
                "options":"Crush Name",
                "reqd": 1,
            },
            {
                "label":"Zone",
                "fieldname":"zone",
                "insert_after":"crush_name",
                "fieldtype":"Data",
                "fetch_from":"crush_name.zone",
                "read_only": 1,
            },
            {
                "fieldname":"member_column_break",
                "insert_after":"zone",
                "fieldtype":"Column Break",
            },
            {
                "label":"Farmer ID",
                "fieldname":"farmer_id",
                "insert_after":"member_column_break",
                "fieldtype":"Data",
                "reqd": 1,
            },
            {
                "label":"Attach Farmer ID",
                "fieldname":"attach_farmer_id",
                "insert_after":"farmer_id",
                "fieldtype":"Attach",
                "reqd": 1,
            },
            {
                "label":"Attach National ID",
                "fieldname":"attach_national_id",
                "insert_after":"attach_farmer_id",
                "fieldtype":"Attach",
                "reqd": 1,
            },
            {
                "label":"Member Account",
                "fieldname":"member_account",
                "insert_after":"attach_national_id",
                "fieldtype":"Section Break",
            },
            {
                "label":"Receivable Accounts",
                "fieldname":"accounts",
                "insert_after":"member_account",
                "fieldtype":"Table",
                "options":"Party Account",
                "reqd": 1,
            }
        ],
    }
    create_custom_fields(fields, update=True)

