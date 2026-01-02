import base64
import io
import qrcode
from odoo import models, fields, api

class Student(models.Model):
    _name = "student.student"
    _description = "Student"
    _rec_name = "full_name"

    full_name = fields.Char(string="Full Name", required=True)
    age = fields.Char(string="Age", required=True)
    name_of_baptism = fields.Char(string="Name of Baptism", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender",default="male")
    parents = fields.Many2many('student.parent', string="Parent")
    phone = fields.Char(string="Phone")
    parents_phone = fields.Char(string="Parents Phone", compute="_compute_parents_phone")
    date_registered = fields.Date(string="Date Registered", default=fields.Date.today())
    photo = fields.Binary(string="Photo")
    id_number = fields.Char(string="ID Number")
    qr_code = fields.Binary(string="QR Code", compute="_compute_qr_code")
    stage_id = fields.Many2one("class.stage",string="Stage")

    @api.model_create_multi
    def create(self, vals_list):
        # Generate a unique ID number for each record
        for vals in vals_list:
            if 'id_number' not in vals or not vals['id_number']:
                vals['id_number'] = self.env['ir.sequence'].next_by_code('student.student.id_number')
        return super().create(vals_list)

    @api.depends('parents')
    def _compute_parents_phone(self):
        for record in self:
            if record.parents:
                phones = [p.phone_no for p in record.parents if p.phone_no]
                record.parents_phone = " / ".join(phones) if phones else ""
            elif record.phone:
                record.parents_phone = record.phone
            else:
                record.parents_phone = ""

    @api.depends("id_number")
    def _compute_qr_code(self):
        for record in self:
            if record.id_number:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(record.id_number)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                record.qr_code = base64.b64encode(buffer.getvalue())
            else:
                record.qr_code = False

    def action_generate_id_badge_pdf(self):
        """Open a URL that will generate and download the badge PDF."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/hr/badge/pdf/{self.id}',
            'target': 'self',
        }