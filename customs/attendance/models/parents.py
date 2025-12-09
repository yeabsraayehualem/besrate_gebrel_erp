from odoo import models,fields,api,_

class Parents(models.Model):
    _inherit="student.parent"


    attendances = fields.One2many('parents.attendance','parent_id')