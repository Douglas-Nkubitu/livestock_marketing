frappe.ui.form.on("Member", {
    refresh: (frm) => {
        frm.set_query('account', 'accounts', function(doc, cdt, cdn) {
            var d  = locals[cdt][cdn];
            var filters = {
                'account_type': 'Receivable',
                'company': d.company,
                "is_group": 0
            };

            if(doc.party_account_currency) {
                $.extend(filters, {"account_currency": doc.party_account_currency});
            }
            return {
                filters: filters
            }
        });
    }
});