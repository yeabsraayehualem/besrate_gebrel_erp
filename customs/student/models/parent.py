from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Parent(models.Model):
    _name = "student.parent"
    _description = "Parent"
    _rec_name = "full_name"

    full_name = fields.Char(string="Full Name", required=True)
    name_of_baptism = fields.Char(string="Name of Baptism", required=True)
    phone_no = fields.Char(string="Phone No", required=True)
    address = fields.Text(string="Address", required=True)
    photo = fields.Binary(string="Photo")