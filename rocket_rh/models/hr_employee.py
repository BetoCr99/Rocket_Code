from odoo import models, fields, api
from datetime import datetime


class HrEmployeeRocket(models.Model):
    _inherit="hr.employee"

    x_age = fields.Integer(string="Edad")
    x_company_tenure = fields.Char(string="Tenencia en la empresa", compute='_compute_company_tenure', store=True)
    x_level = fields.Many2one(
        string="Nivel jerárquico",
        comodel_name="hr.level",
    )
    x_contract_type = fields.Selection(
        selection=[
            ("permanent", "Permanente"),
            ("temporary", "Temporal"),
            ("freelance", "Freelance"),
        ],
        string="Tipo de contrato",
    )
    linkedin_url = fields.Char(string="LinkedIn", help="https://linkedin.com/in/username")
    cv_file = fields.Binary(attachment=True)
    x_building_access_card = fields.Char(string="Tarjeta de acceso al edificio", help="Ingrese el número de la tarjeta de acceso")
    x_parking_access_id = fields.Char(string="ID de acceso al estacionamiento", help="Ingrese el ID de acceso al estacionamiento")
    rfc = fields.Char(string="RFC")
    nda = fields.Binary(string="NDA", attachment=True)
    privacy_notice = fields.Binary(string="Aviso de privacidad", attachment=True)

    @api.depends('create_date')
    def _compute_company_tenure(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                current_date = fields.Datetime.now()
                delta = current_date - create_date
                years = delta.days // 365
                months = (delta.days % 365) // 30  
                record.x_company_tenure = f"{years} años {months} meses"


class HrLevel(models.Model):
    _name = "hr.level"
    _description = "Niveles Jerárquicos"

    name = fields.Char(string="Nombre del Nivel", required=True)
    code = fields.Char(string="Código", help="Código único para identificar el nivel.")
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=True)

