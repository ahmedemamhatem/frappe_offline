from . import __version__ as app_version

app_name = "frappe_offline"
app_title = "Frappe Offline"
app_publisher = "Ahmed Emam"
app_description = "Frappe Sync"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ahmedemamhatem@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_offline/css/frappe_offline.css"
# app_include_js = "/assets/frappe_offline/js/frappe_offline.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_offline/css/frappe_offline.css"
# web_include_js = "/assets/frappe_offline/js/frappe_offline.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_offline/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_offline.install.before_install"
# after_install = "frappe_offline.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_offline.uninstall.before_uninstall"
# after_uninstall = "frappe_offline.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_offline.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "after_insert": "frappe_offline.frappe_offline.doctype.frappe_sync.frappe_sync.notify_sync",
        "on_update": "frappe_offline.frappe_offline.doctype.frappe_sync.frappe_sync.notify_sync",
        "on_cancel": "frappe_offline.frappe_offline.doctype.frappe_sync.frappe_sync.notify_sync",
        "on_trash": "frappe_offline.frappe_offline.doctype.frappe_sync.frappe_sync.notify_sync",
    }
}	

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"frappe_offline.tasks.all"
#	],
#	"daily": [
#		"frappe_offline.tasks.daily"
#	],
#	"hourly": [
#		"frappe_offline.tasks.hourly"
#	],
#	"weekly": [
#		"frappe_offline.tasks.weekly"
#	]
#	"monthly": [
#		"frappe_offline.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "frappe_offline.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "frappe_offline.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "frappe_offline.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["frappe_offline.utils.before_request"]
# after_request = ["frappe_offline.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_offline.utils.before_job"]
# after_job = ["frappe_offline.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"frappe_offline.auth.validate"
# ]

