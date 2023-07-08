// Copyright (c) 2023, Douglas Nkubitu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kill Sheet', {
    refresh: function(frm){
        if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Payment'),
				function () {
					frm.events.make_payment_entry(frm);
				}, __('Create'));
		}
    },
    make_payment_entry: function(frm) {
		let method = "livestock_marketing.overrides.customer_payment_entry.get_payment_entry_for_customer";
	
		return frappe.call({
			method: method,
			args: {
				"dt": frm.doc.doctype,
				"dn": frm.doc.name
			},
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},
})

frappe.ui.form.on('Kill Sheet', {
	refresh: function(frm) {
        if (frm.is_new()) {
            frm.set_value('posting_time', frappe.datetime.now_time());
        }
    },

    //Get livestock loaded details
    livestock_loading: function (frm) {
        if (frm.doc.livestock_loading) {
            frm.clear_table('livestock_kill_sheet');
            frappe.model.with_doc('Livestock Loading', frm.doc.livestock_loading, function () {
                let source_doc = frappe.model.get_doc('Livestock Loading', frm.doc.livestock_loading);
                $.each(source_doc.livestock_loading, function (index, source_row) {
                    if (source_row.status === 'Accepted') {
                        const target_row = frm.add_child('livestock_kill_sheet');
                        target_row.ear_tag = source_row.ear_tag;
                        target_row.shape = source_row.shape;
                        target_row.cattle_brand = source_row.cattle_brand;
                        target_row.breed = source_row.breed;
                        target_row.gender = source_row.gender;
                        target_row.status = source_row.status;
                    }
                });
                frm.refresh_field('livestock_kill_sheet');
            });
        }
    },

    //Calculate total Amount
    validate: function (frm) {
        //Calculate Total Amount
        var totalAmount = 0;
        // Iterate over each row in the child table
        frm.doc.livestock_kill_sheet.forEach(function(row) {
        totalAmount += row.amount;
        });
        // Set the total amount in the field
        frm.set_value('total_amount', totalAmount);

        //Calculate Total Amount
        var netAmount = frm.doc.total_amount;
      
        // Iterate over each row in the child table and subtract the amount
        frm.doc.livestock_kill_sheet.forEach(function(row) {
          netAmount -=  frm.doc.amount;
        });
        // Set the total amount in the field
        frm.set_value('net_amount', netAmount);

        //Calculate Total Weight
        var totalWeight =0;
         // Iterate over each row in the child table
        frm.doc.livestock_kill_sheet.forEach(function(row){
        totalWeight += row.qty;
        })
        // Set the total qty in the field
        frm.set_value('total_qty', totalWeight)
	}
});

//Amount Calculation
var amount_calculation = function (frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if ((row.qty) && (row.rate)) {
        frappe.model.set_value(cdt, cdn, 'amount', (row.qty * row.rate));
        frm.refresh_field("amount");
    }
}

//Child table amount calculation on qty change
frappe.ui.form.on("Livestock Kill sheet", "qty", function (frm, cdt, cdn) {
    //amount on qty change
    amount_calculation(frm, cdt, cdn);
})

//Child table amount calculation on rate change
frappe.ui.form.on("Livestock Kill sheet", "rate", function (frm, cdt, cdn) {
    //amount on cost change
    amount_calculation(frm, cdt, cdn);
})