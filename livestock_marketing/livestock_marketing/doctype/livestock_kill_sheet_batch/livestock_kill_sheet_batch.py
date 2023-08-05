# Copyright (c) 2023, Douglas Nkubitu and contributors
# For license information, please see license.txt

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
				'total_amount_payable': data.total_amount_payable                       
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
        SELECT DISTINCT lks.name, lks.farmer_name, lks.posting_date, lks.net_amount, lks.total_deductions, lks.total_amount_payable
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