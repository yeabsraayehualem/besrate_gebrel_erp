from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError


class Courses(models.Model):
    _name="class.course"
    _description="Course"
    

    name = fields.Char(string="Title",required=True)
    image = fields.Binary(string="Image")
    pdf_book = fields.Binary(string="Text Book")
    stage_id = fields.Many2one('class.stage',string="Stage")
    semister = fields.Selection([('1','Semister 1'),('2','Semister 2')],string="Semister")