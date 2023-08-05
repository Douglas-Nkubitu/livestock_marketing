// Copyright (c) 2023, Douglas Nkubitu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Livestock Kill Sheet Batch', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Journal Entry'), function() {
                frm.events.create_journal_entry_from_js(frm);
            }, __('Create Journal Entry'));
        }
    },
    create_journal_entry_from_js: function(frm) {
        frappe.call({
            method: 'livestock_marketing.livestock_marketing.doctype.livestock_kill_sheet_batch.livestock_kill_sheet_batch.create_journal_entry',
            args: {
                kill_sheet_batch: frm.doc.name
            },
            callback: function(response) {
                // Optional: Handle the response or show a message
                frappe.msgprint('Journal Entry created successfully!');
                // Optional: Refresh the form to update the Journal Entry link field
                frm.reload_doc();
            }
        });
    }
});

frappe.ui.form.on('Livestock Kill Sheet Batch', {
    //selecting and adding livestock kill sheet in child table
    get_livestock_kill_sheet: function (frm) {
		frappe.call({
			method: "get_submitted_livestock_kill_sheet",
			doc: frm.doc,
			callback: function (r) {
				refresh_field("livestock_kill_sheet_batch");
			}
		});
	},

	//Calculate total Amount
    validate: function (frm) {
        //Calculate Net Amount
        var netAmount = 0;
        // Iterate over each row in the child table
        frm.doc.livestock_kill_sheet_batch.forEach(function(row) {
		netAmount += row.net_amount;
        });
        // Set the net amount in the field
        frm.set_value('amount', netAmount);

        //Calculate Total Deduction
        var totalDeductions = 0;
		// Iterate over each row in the child table
        frm.doc.livestock_kill_sheet_batch.forEach(function(row) {
			totalDeductions += row.total_deductions;
			});
        // Set the total deductions in the field
        frm.set_value('deductions', totalDeductions);

        //Calculate Total Payable Amount
        var totalPayable =0;
         // Iterate over each row in the child table
        frm.doc.livestock_kill_sheet_batch.forEach(function(row){
		totalPayable += row.total_amount_payable;
        })
        // Set the total payable in the field
        frm.set_value('amount_payable', totalPayable);
	}
});