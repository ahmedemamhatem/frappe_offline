
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
class FrappeSync(Document):
	def before_insert(self):
		self.check_url()
		self.create_custom_fields()
	
 	
	def validate(self):
		self.check_url()
		self.create_custom_fields()
  
	def check_url(self):
		valid_url_schemes = ("http", "https")
		frappe.utils.validate_url(self.remote_site_url, throw=True, valid_schemes=valid_url_schemes)

		# remove '/' from the end of the url like http://test_site.com/
		# to prevent mismatch in get_url() results
		if self.remote_site_url.endswith("/"):
			self.remote_site_url = self.remote_site_url[:-1]
   
	def create_custom_fields(self):
		"""create custom field to store remote docname and remote site url"""
		for entry in self.doctype_to_sync:
			if not entry.use_same_name:
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
				