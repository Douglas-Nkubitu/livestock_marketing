// Copyright (c) 2023, Douglas Nkubitu and contributors
// For license information, please see license.txt

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
        frm.set_value('net_amount', netAmount);

        //Calculate Total Deduction
        var totalDeductions = 0;
		// Iterate over each row in the child table
        frm.doc.livestock_kill_sheet_batch.forEach(function(row) {
			totalDeductions += row.total_deductions;
			});
        // Set the total deductions in the field
        frm.set_value('total_deductions', totalDeductions);

        //Calculate Total Payable Amount
        var totalPayable =0;
         // Iterate over each row in the child table
        frm.doc.livestock_kill_sheet_batch.forEach(function(row){
		totalPayable += row.total_amount_payable;
        })
        // Set the total payable in the field
        frm.set_value('total_amount_payable', totalPayable);
	}
});