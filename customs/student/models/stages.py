from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError



class Stages(models.Model):
    _name="class.stage"
    
    name=fields.Char(string="Name",required=True)
    courses = fields.One2many("class.course","stage_id")
    courses_number = fields.Integer(string="Courses Number",compute="_compute_courses_numeber")
    
    @api.depends('courses')
    def _compute_courses_numeber(self):
        for record in self:
            record.courses_number = len(record.courses)