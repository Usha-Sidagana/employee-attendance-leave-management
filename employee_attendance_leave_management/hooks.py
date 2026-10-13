app_name = "employee_attendance_leave_management"
app_title = "Employee Attendance and Leave Management"
app_publisher = "Usha Sidagana"
app_description = "Employee Attendance and Leave Management"
app_email = "ushasidagana01@gmail.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["erpnext", "hrms"]

after_migrate = "employee_attendance_leave_management.setup.after_migrate"

doc_events = {
	"Employee Checkin": {"on_update": "employee_attendance_leave_management.attendance_utils.on_checkin_save"}
}

permission_query_conditions = {
	"Attendance Correction Request": ("employee_attendance_leave_management.permissions.correction_query"),
}

has_permission = {
	"Attendance Correction Request": (
		"employee_attendance_leave_management.permissions.correction_has_permission"
	),
}

fixtures = [
	{
		"dt": "Custom DocPerm",
		"filters": [["parent", "=", "Attendance Correction Request"]],
	},
	{
		"dt": "Property Setter",
		"filters": [["doc_type", "=", "Attendance Correction Request"]],
	},
]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "employee_attendance_leave_management",
# 		"logo": "/assets/employee_attendance_leave_management/logo.png",
# 		"title": "Employee Attendance and Leave Management",
# 		"route": "/employee_attendance_leave_management",
# 		"has_permission": "employee_attendance_leave_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/employee_attendance_leave_management/css/employee_attendance_leave_management.css"
# app_include_js = "/assets/employee_attendance_leave_management/js/employee_attendance_leave_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/employee_attendance_leave_management/css/employee_attendance_leave_management.css"
# web_include_js = "/assets/employee_attendance_leave_management/js/employee_attendance_leave_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "employee_attendance_leave_management/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "employee_attendance_leave_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "employee_attendance_leave_management.utils.jinja_methods",
# 	"filters": "employee_attendance_leave_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "employee_attendance_leave_management.install.before_install"
# after_install = "employee_attendance_leave_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "employee_attendance_leave_management.uninstall.before_uninstall"
# after_uninstall = "employee_attendance_leave_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "employee_attendance_leave_management.utils.before_app_install"
# after_app_install = "employee_attendance_leave_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "employee_attendance_leave_management.utils.before_app_uninstall"
# after_app_uninstall = "employee_attendance_leave_management.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "employee_attendance_leave_management.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "employee_attendance_leave_management.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["employee_attendance_leave_management.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"employee_attendance_leave_management.tasks.all"
# 	],
# 	"daily": [
# 		"employee_attendance_leave_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"employee_attendance_leave_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"employee_attendance_leave_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"employee_attendance_leave_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "employee_attendance_leave_management.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "employee_attendance_leave_management.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "employee_attendance_leave_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "employee_attendance_leave_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["employee_attendance_leave_management.utils.before_request"]
# after_request = ["employee_attendance_leave_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["employee_attendance_leave_management.utils.before_job"]
# after_job = ["employee_attendance_leave_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"employee_attendance_leave_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
