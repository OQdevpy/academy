from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError
from datetime import timedelta

class Employee(models.Model):
    _inherit = "res.users"
    _description = "Employee"

    role = fields.Selection(
        [
            ("admin", "Admin"),
            ("administrator", "Administrator"),
        ],
        string="Role",
        default="admin",
    )

    urole = fields.Selection(
        [
            ("admin", "Admin"),
            ("administrator", "Administrator"),
        ],
        compute="_compute_user_role",
        store=False,
    )

    address = fields.Text(string="Address")
    phone_number = fields.Char(string="Phone Number")

    def action_change_password(self):
        self.ensure_one()

        return {
            "name": "Change Password",
            "type": "ir.actions.act_window",
            "res_model": "change.password.wizard",
            "view_mode": "form",
            "target": "new",
        }

    @api.model
    def create(self, vals):
        employee = super(Employee, self).create(vals)

        if vals.get("role") == "adminstrator":
            admin_group = self.env.ref("academy.group_administrator")
            employee.groups_id = [(4, admin_group.id)]
        elif vals.get("role") == "admin":
            admin_group = self.env.ref("academy.group_admin")
            employee.groups_id = [(4, admin_group.id)]
        return employee

    def write(self, vals):
        res = super(Employee, self).write(vals)

        if vals.get("role") == "adminstrator":
            admin_group = self.env.ref("academy.group_administrator")
            self.groups_id = [(4, admin_group.id)]
        elif vals.get("role") == "admin":
            admin_group = self.env.ref("academy.group_administrator")
            self.groups_id = [(3, admin_group.id)]

        if vals.get("role") == "admin":
            admin_group = self.env.ref("academy.group_admin")
            self.groups_id = [(4, admin_group.id)]
        elif vals.get("role") == "adminstrator":
            admin_group = self.env.ref("academy.group_admin")
            self.groups_id = [(3, admin_group.id)]

        return res

    @api.depends("user_id")  # Assuming user_id is the field linking to the user
    def _compute_user_role(self):
        print("Computing user role")
        for record in self:
            # Check if the current user is an admin
            if self.env.user.has_group("base.group_system"):
                record.urole = "admin"
            else:
                record.urole = "administrator"


class Group(models.Model):
    _name = "education.group"
    _description = "Group"

    name = fields.Char(string="Group Name", required=True)
    course_id = fields.Many2one("education.course", string="Course", required=True)
    teacher_id = fields.Many2one("education.teacher", string="Teacher", required=True)
    student_ids = fields.Many2many("education.student", string="Students")
    payment_ids = fields.One2many(
        "education.payment", "group_id", string="Payments"
    )  

class Course(models.Model):
    _name = "education.course"
    _description = "Course"

    name = fields.Char(string="Course Name", required=True, translate=True)
    description = fields.Text(string="Description")
    duration = fields.Integer(
        string="Duration (in hours)"
    )  # Changed from 'davomiylik' to 'duration'
    active_cource = fields.Boolean(string="Is Active", default=True)


class Teacher(models.Model):
    _name = "education.teacher"
    _description = "Teacher"

    name = fields.Char(string="Name", store=True)
    course_ids = fields.Many2many("education.course", string="Courses")
    phone_number = fields.Char(string="Phone Number")
    payout_ids = fields.One2many(
        "education.payout", "employee_id", string="payouts"
    )  


class Student(models.Model):
    _name = "education.student"
    _description = "Student"

    name = fields.Char(string="Student Name", required=True)
    payment_ids = fields.One2many(
        "education.payment", "student_id", string="Payments"
    )  
    phone_number = fields.Char(string="Phone Number")


class Payment(models.Model):
    _name = "education.payment"
    _description = "Payment"

    student_id = fields.Many2one("education.student", string="Student", required=True)
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Date", required=True)
    description = fields.Text(string="Description")
    group_id = fields.Many2one(
        "education.group", string="Group"
    )  # Changed from 'group' to 'group_id'

    # is_recent_payment = fields.Boolean(string="Is Recent Payment", compute="_compute_is_recent_payment", store=False)

    # @api.depends('date')
    # def _compute_is_recent_payment(self):
        
    #     """Mark payments from the last 7 days as recent"""
    #     today = fields.Date.today()
    #     for record in self:
    #         if record.date:
    #             record.is_recent_payment = record.date >= today - timedelta(minutes=1)
    #         else:
    #             record.is_recent_payment = False

class Payout(models.Model):
    _name = "education.payout"
    _description = "Payout"

    employee_id = fields.Many2one("education.teacher", string="Employee", required=True)
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Date", required=True)
    description = fields.Text(string="Description")


class Attendance(models.Model):
    _name = "education.attendance"
    _description = "Attendance"

    group_id = fields.Many2one("education.group", string="Group", required=True)
    date = fields.Date(string="Date", required=True)
    student_ids = fields.Many2many(
        "education.student", string="Students", required=True
    )
    is_present = fields.Boolean(string="Is Present", default=True)
