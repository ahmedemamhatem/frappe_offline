frappe.ui.form.on('Frappe Sync', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Add custom buttons for validation
            frm.add_custom_button(__('Validate Remote DocTypes'), function() {
                checkRemoteDocTypes(frm);
            });
            frm.add_custom_button(__('Validate Remote Connection'), function() {
                checkRemoteConnection(frm);
            });
        }
    }
});

function checkRemoteConnection(frm) {
    frappe.call({
        method: 'check_remote_connection',
        doc: frm.doc,
        args: {},
        freeze: true,
        freeze_message: "Testing connection...",
        callback: function(response) {
            if (response && response.message) {
                frappe.msgprint(response.message);
            } else {
                frappe.msgprint("No response from the server.");
            }
        }
    });
}

function checkRemoteDocTypes(frm) {
    frappe.call({
        method: 'create_remote_custom_fields',
        doc: frm.doc,
        args: {},
        freeze: true,
        freeze_message: 'Validating remote DocTypes...',
        callback: function(response) {
            frappe.show_alert({
                message: __('Job enqueued'),
                indicator: 'green'
            });
        }
    });
}

frappe.ui.form.on("Frappe Sync", {
	refresh: function (frm) {
		frm.set_query("doctype_to_sync", "doctype_to_sync", function () {
			return {
				filters: {
					issingle: 0,
					istable: 0,
				},
			};
		});

		frm.set_indicator_formatter("status", function (doc) {
			let indicator = "orange";
			if (doc.status == "Approved") {
				indicator = "green";
			} else if (doc.status == "Rejected") {
				indicator = "red";
			}
			return indicator;
		});
	},
});