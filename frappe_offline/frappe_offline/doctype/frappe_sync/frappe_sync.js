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
        method: 'frappe_offline.doctype.frappe_sync.frappe_sync.check_remote_doctypes',
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
