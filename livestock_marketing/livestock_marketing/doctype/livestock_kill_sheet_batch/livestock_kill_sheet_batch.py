# Copyright (c) 2023, Douglas Nkubitu and contributors
# For license information, please see license.txt

from frappe.utils import get_url_to_form
import frappe
from frappe import _
from frappe.model.document import Document

class LivestockKillSheetBatch(Document):
	# Get submitted Kill sheets
	@frappe.whitelist()
	def get_submitted_livestock_kill_sheet(self):
		#Validations
		if not self.from_date:
			frappe.throw(_("Please select the From Date Filter"),title=_("From Date Required"))

		if not self.to_date:
			frappe.throw(_("Please select the To Date Filter"),title=_("To Date Required"))
		#End Validations

		""" Pull livestock kill sheet which are submitted based on criteria selected"""
		submitted_livestock_kill_sheet = get_livestock_kill_sheet(self)

		if submitted_livestock_kill_sheet:
			self.get_livestock_kill_sheet_in_table(submitted_livestock_kill_sheet)
			self.get_items()
			frappe.msgprint(_("Livestock Kill Sheet Selection Completed"),title=_("Livestock Kill Sheet Selection"))
		else:
			frappe.msgprint(_("Livestock Kill Sheets are not available for Livestock Kill Sheet Batch"))
	
	# Add submitted livestock kill sheets in table
	def get_livestock_kill_sheet_in_table(self, submitted_livestock_kill_sheet): 
		""" Add livestock kill sheets in the table"""
		self.set('livestock_kill_sheet_batch', [])
		for data in submitted_livestock_kill_sheet:
			self.append('livestock_kill_sheet_batch', {
				'livestock_kill_sheet': data.name,
				'farmer_name': data.farmer_name,
				'net_amount': data.net_amount,
				'total_deductions':data.total_deductions,
				'total_amount_payable': data.total_amount_payable,
				'commission_amount': data.amount                       
			})

	# Get Items
	def get_items(self):
		self.get_lksb_items()

	# Get list of livestock kill sheet query
	def get_lksb_items(self):
		# Check for empty table or empty rows
		if not self.get("livestock_kill_sheet_batch"):
			frappe.throw(_("Please fill the Kill Sheet Details table"),
							title=_("Livestock Kill Sheet Items Required"))

# Get submitted livestock kill sheet query
def get_livestock_kill_sheet(self):
    lksb_filter = ""
    params = {}

    if self.from_date:
        lksb_filter += " and lks.posting_date >= %(from_date)s"
        params["from_date"] = self.from_date

    if self.to_date:
        lksb_filter += " and lks.posting_date <= %(to_date)s"
        params["to_date"] = self.to_date

    submitted_livestock_kill_sheet = frappe.db.sql("""
        SELECT DISTINCT lks.name, lks.farmer_name, lks.posting_date, lks.amount, lks.net_amount, lks.total_deductions, lks.total_amount_payable
        FROM `tabLivestock Kill Sheet` lks
        WHERE lks.docstatus = 1
        AND (
            lks.name NOT IN (
                SELECT lksbd.livestock_kill_sheet
                FROM `tabLivestock Kill Sheet Batch Details` lksbd,	
						   `tabLivestock Kill Sheet Batch` lksb
                WHERE lksbd.parent = lksb.name 
						   AND lksb.docstatus != 2
            )
        )
        {}
        ORDER BY lks.name
    """.format(lksb_filter), params, as_dict=True)
    
    return submitted_livestock_kill_sheet

@frappe.whitelist()
def create_journal_entry(kill_sheet_batch):
	# Retrieve child table records from "Livestock Kill Sheet Batch Details"
	child_records = frappe.get_doc("Livestock Kill Sheet Batch", kill_sheet_batch)

	# Calculate the total_amount_payable from debtors
	total_amount = sum(child_record.total_amount_payable for child_record in child_records.get("livestock_kill_sheet_batch"))

	# Store the parent_docname for later use
	parent_docname = child_records.name

	# Create a new Journal Entry
	journal_entry = frappe.new_doc("Journal Entry")
	journal_entry.voucher_type = "Journal Entry"
	journal_entry.posting_date = frappe.utils.today()
	journal_entry.company = frappe.defaults.get_defaults().get("company")

	# Create a new Journal Entry account row for "Cash - S"
	cash_account_row = frappe.new_doc("Journal Entry Account")
	cash_account_row.account = "Cash - S"  # Replace with the appropriate account name
	cash_account_row.credit_in_account_currency = total_amount

	# Append the "Cash - S" account row to the Journal Entry
	journal_entry.append("accounts", cash_account_row)
	for child_record in child_records.get("livestock_kill_sheet_batch"):
		farmer_name = child_record.farmer_name
		total_amount_payable = child_record.total_amount_payable

		# Create a new Journal Entry account row for "Debtors - S" linked to the farmer
		debtor_account_row = frappe.new_doc("Journal Entry Account")
		debtor_account_row.account = "Debtors - S"  # Replace with the appropriate account name
		debtor_account_row.party_type = "Customer"
		debtor_account_row.party = farmer_name
		debtor_account_row.user_remark = f"Journal Entry created from {parent_docname}"
		debtor_account_row.debit_in_account_currency = total_amount_payable

		# Append the "Debtors - S" account row to the Journal Entry
		journal_entry.append("accounts", debtor_account_row)

		# # Print the data before creating the Journal Entry (optional)
		# frappe.msgprint(f"Farmer Name: {farmer_name}, Total Amount Payable: {total_amount_payable}")

	journal_entry.cheque_no = ""  
	journal_entry.cheque_date = ""
	journal_entry.user_remark = f"Journal Entry created from {parent_docname} Batch"
	journal_entry.remark = f"Journal Entry created from {parent_docname} Batch"
	journal_entry.insert(ignore_permissions=True)
	journal_entry.save()
	jv_url = get_url_to_form(journal_entry.doctype, journal_entry.name)
	jv_msgprint = f"Journal Entry Created <a href='{jv_url}'>{journal_entry.name}</a>"
	frappe.msgprint(_(jv_msgprint))

	return journal_entry.name