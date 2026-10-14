import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_install():
	# HRMS hides In Time / Out Time unless a shift is set. Always show them.
	for fieldname in ("in_time", "out_time"):
		make_property_setter("Attendance", fieldname, "depends_on", "", "Data")
	frappe.db.commit()
