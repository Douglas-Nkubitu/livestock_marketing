// Copyright (c) 2023, Douglas Nkubitu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kill Sheet', {
	refresh: function(frm) {
        if (frm.is_new()) {
            frm.set_value('posting_time', frappe.datetime.now_time());
        }
    }
});
