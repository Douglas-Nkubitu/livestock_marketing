// Copyright (c) 2023, Douglas Nkubitu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Livestock Loading', {
	refresh: function(frm) {
        if (frm.is_new()) {
            frm.set_value('posting_time', frappe.datetime.now_time());
        }
    },
    //Get livestock details
    livestock_registration: function (frm) {
        if (frm.doc.livestock_registration) {
            frm.clear_table('livestock_loading');
            frappe.model.with_doc('Livestock Registration', frm.doc.livestock_registration, function () {
                let source_doc = frappe.model.get_doc('Livestock Registration', frm.doc.livestock_registration);
                $.each(source_doc.livestock_details, function (index, source_row) {
					const target_row = frm.add_child('livestock_loading');
                    target_row.ear_tag = source_row.ear_tag;
                    target_row.shape = source_row.shape;
                    target_row.cattle_brand = source_row.cattle_brand;
                    target_row.breed = source_row.breed;
                    target_row.gender = source_row.gender;
                    frm.refresh_field('livestock_loading');
                });
            });
        }
    },
});
