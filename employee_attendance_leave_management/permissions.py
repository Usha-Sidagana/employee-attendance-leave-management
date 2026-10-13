import frappe

DOCTYPE = "Attendance Correction Request"

HR_ROLES = {"HR Manager", "HR User"}
MANAGER_ROLES = {"Manager"}


def get_user_employee(user):
    """Return the Employee linked to the logged-in user."""
    return frappe.db.get_value(
        "Employee",
        {"user_id": user},
        "name",
    )


def correction_query(user):
    """Filter requests according to employee, manager, or HR access."""
    user = user or frappe.session.user

    if user == "Administrator":
        return None

    roles = set(frappe.get_roles(user))

    if "System Manager" in roles or HR_ROLES.intersection(roles):
        return None

    employee = get_user_employee(user)

    if not employee:
        return "1=0"

    employees = [employee]

    if MANAGER_ROLES.intersection(roles):
        reports = frappe.get_all(
            "Employee",
            filters={"reports_to": employee},
            pluck="name",
        )
        employees.extend(reports)

    employee_names = ", ".join(
        frappe.db.escape(name) for name in set(employees)
    )

    return f"`tab{DOCTYPE}`.`employee` IN ({employee_names})"


def correction_has_permission(
    doc,
    user=None,
    permission_type=None,
):
    """Enforce individual document access."""
    user = user or frappe.session.user
    permission_type = permission_type or "read"

    if user == "Administrator":
        return True

    roles = set(frappe.get_roles(user))

    if "System Manager" in roles or HR_ROLES.intersection(roles):
        return True

    employee = get_user_employee(user)

    if not employee:
        return False

    # Employees may read their own requests, but cannot approve/reject them.
    if doc.employee == employee:
        if permission_type in ("read", "select"):
            return True

        if doc.is_new() and permission_type in ("create", "write"):
            return True

        return False

    # Managers can access requests belonging to direct reports.
    if MANAGER_ROLES.intersection(roles):
        is_direct_report = frappe.db.exists(
            "Employee",
            {
                "name": doc.employee,
                "reports_to": employee,
            },
        )

        if is_direct_report:
            return permission_type in (
                "read",
                "write",
                "select",
            )

    return False
