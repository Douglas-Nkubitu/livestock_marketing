import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields={
        "Customer": [
            {
                "label":"Member Details",
                "fieldname":"members_details",
                "insert_after":"image",
                "fieldtype":"Section Break",
            },
            {
                "label":"Customer Categories",
                "fieldname":"customer_categories",
                "fieldtype":"Select",
                "options": "\nMember\nNon Member",
                "insert_after":"members_details",
                "reqd": 1,
            },
            {
                "label":"Crush Name",
                "fieldname":"crush_name",
                "insert_after":"customer_categories",
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
            }
        ],
    }
    create_custom_fields(fields, update=True)

