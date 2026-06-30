from odoo import models, fields

class Job(models.Model):
    _inherit = 'hr.job'

    work_activity = fields.Html(string='Work Activity')
    kpi = fields.Html(string='KPI')
