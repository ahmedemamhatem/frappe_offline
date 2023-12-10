import json
import time
import requests
import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from frappe.frappeclient import FrappeClient
from frappe.model.document import Document
from frappe.utils.background_jobs import get_jobs
from frappe.utils.data import get_link_to_form, get_url
from frappe.utils.password import get_decrypted_password
from frappe_offline.frappeclient import FrappeClient
from frappe.utils.password import get_decrypted_password


# Define a custom Document class FrappeSync
class FrappeSync(Document):
	
	# Whitelisted method to check the remote connection
	@frappe.whitelist()
	def check_remote_connection(doc):
		# Accessing attributes from the document
		remote_site_url = doc.remote_site_url
		frappe_user_name = doc.frappe_user_name if doc.frappe_user_name else doc.frappe_api_key
		frappe_user_password=doc.get_password("frappe_user_password") or doc.get_password("frappe_api_secret")
		
		try:
			# Attempt to establish a connection to the remote site
			conn = FrappeClient(remote_site_url)
			login_success = conn.login(frappe_user_name, frappe_user_password)
			
			# Check if connected or not and return a message
			if login_success:
				frappe.msgprint("Connected to Frappe server!")
			else:
				frappe.msgprint("Connection failed. Please check your credentials.")
		except Exception as e:
			frappe.msgprint(f"Authentication Error")

	# Whitelisted method to be executed before insert
	@frappe.whitelist()
	def before_insert(doc):
		if doc.enable == 1:
			doc.check_url()
			doc.create_custom_fields()
			doc.create_remote_custom_fields()

	# Validation method for the document
	@frappe.whitelist()
	def validate(doc):
		if doc.enable == 1:
			doc.check_url()
			doc.create_custom_fields()
			doc.create_remote_custom_fields()
  
	# Method to check the validity of the URL
	@frappe.whitelist()
	def check_url(doc):
		if doc.remote_site_url:
			valid_url_schemes = ("http", "https")
			frappe.utils.validate_url(doc.remote_site_url, throw=True, valid_schemes=valid_url_schemes)

			# Remove '/' from the end of the URL
			if doc.remote_site_url.endswith("/"):
				doc.remote_site_url = doc.remote_site_url[:-1]
   
	# Method to create custom fields for remote document sync
	@frappe.whitelist()
	def create_custom_fields(doc):
		for entry in doc.doctype_to_sync:
			if entry.doctype_to_sync:
				# Create custom field "remote_sync" if it doesn't exist
				if not frappe.db.exists(
					"Custom Field", {"fieldname": "remote_sync", "dt": entry.doctype_to_sync}
				):
					df = dict(
						fieldname="remote_sync",
						label="Remote Document Synced",
						fieldtype="Check",
						read_only=1,
						print_hide=1,
						hidden=1,
						default=0,
					)
					create_custom_field(entry.doctype_to_sync, df)
				
				# Create custom field "remote_sync_site" if it doesn't exist
				if not frappe.db.exists(
					"Custom Field", {"fieldname": "remote_sync_site", "dt": entry.doctype_to_sync}
				):
					df = dict(
						fieldname="remote_sync_site",
						label="Remote Sync Site",
						fieldtype="Data",
						read_only=1,
						print_hide=1,
						hidden=1,
					)
					create_custom_field(entry.doctype_to_sync, df)
	
 
	# Method to create custom fields for remote server
	@frappe.whitelist()
	def create_remote_custom_fields(doc):

		remote_site_url = doc.remote_site_url
		frappe_user_name = doc.frappe_user_name if doc.frappe_user_name else doc.frappe_api_key
		frappe_user_password=doc.get_password("frappe_user_password") or doc.get_password("frappe_api_secret")
		try:
			# Attempt to establish a connection to the remote site
			conn = FrappeClient(remote_site_url)
			conn.login(frappe_user_name, frappe_user_password)
			login_success = conn.login(frappe_user_name, frappe_user_password)

			# Check if connected or not and proceed accordingly
			if login_success:
				for entry in doc.doctype_to_sync:
					if entry.doctype_to_sync and entry.enable == 1 and (not entry.remote_validated or entry.remote_validated == "No"):
						fields_to_check = ['remote_sync', 'remote_sync_site']
						for field in fields_to_check:
							frappe.db.set_value('Doctype to Sync', entry.name, 'remote_validated', 'No')
							# Create custom field if it doesn't exist
							if not conn.get_list('Custom Field', fields=['name'], filters={'fieldname': field, 'dt': entry.doctype_to_sync}):
								try:
									fieldtype = "Check" if field == 'remote_sync' else "Data"
									conn.insert({
										"doctype": "Custom Field",
										"dt": entry.doctype_to_sync,
										"fieldname": field,
										"label": "Remote Sync" if field == 'remote_sync' else "Remote Sync Site",
										"fieldtype": fieldtype,
										"read_only": 1,
										"print_hide": 1,
										"hidden": 1
									})
									frappe.db.set_value('Doctype to Sync', entry.name, 'remote_validated', 'Yes')
								except Exception as e:
									frappe.msgprint(f"Failed to create {field} field: {str(entry.doctype_to_sync)}")
							if conn.get_list('Custom Field', fields=['name'], filters={'fieldname': field, 'dt': entry.doctype_to_sync}):
								frappe.db.set_value('Doctype to Sync', entry.name, 'remote_validated', 'Yes')
           
			else:
				# Throw a connection error if unable to connect to the remote site
				raise ConnectionError("Unable to establish a connection to the remote site.")
		except ConnectionError as e:
			frappe.throw("Authentication Error")  # Throw connection error message in Frappe
