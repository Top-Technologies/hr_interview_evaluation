from odoo import api, fields, models


class HrApplicant(models.Model):
    """Extend hr.applicant to include evaluations list and computed averages."""
    _inherit = 'hr.applicant'

    evaluation_ids = fields.One2many(
        comodel_name='hr.interview.evaluation',
        inverse_name='applicant_id',
        string='Interview Evaluations',
    )

    evaluation_avg_personality = fields.Float(
        string='Avg Personality',
        compute='_compute_evaluation_averages',
        store=True,
    )
    evaluation_avg_hard_skill = fields.Float(
        string='Avg Hard Skill',
        compute='_compute_evaluation_averages',
        store=True,
    )
    evaluation_avg_communication = fields.Float(
        string='Avg Communication',
        compute='_compute_evaluation_averages',
        store=True,
    )
    evaluation_avg_teamwork = fields.Float(
        string='Avg Team Work',
        compute='_compute_evaluation_averages',
        store=True,
    )
    evaluation_avg_total = fields.Float(
        string='Avg Total Score',
        compute='_compute_evaluation_averages',
        store=True,
    )
    evaluation_count = fields.Integer(
        string='Evaluators',
        compute='_compute_evaluation_averages',
        store=True,
    )

    @api.depends(
        'evaluation_ids.score_personality',
        'evaluation_ids.score_hard_skill',
        'evaluation_ids.score_communication',
        'evaluation_ids.score_teamwork',
        'evaluation_ids.score_total',
    )
    def _compute_evaluation_averages(self):
        for rec in self:
            evals = rec.evaluation_ids
            count = len(evals)
            rec.evaluation_count = count
            if count > 0:
                rec.evaluation_avg_personality = (
                    sum(evals.mapped('score_personality')) / count
                )
                rec.evaluation_avg_hard_skill = (
                    sum(evals.mapped('score_hard_skill')) / count
                )
                rec.evaluation_avg_communication = (
                    sum(evals.mapped('score_communication')) / count
                )
                rec.evaluation_avg_teamwork = (
                    sum(evals.mapped('score_teamwork')) / count
                )
                rec.evaluation_avg_total = (
                    sum(evals.mapped('score_total')) / count
                )
            else:
                rec.evaluation_avg_personality = 0.0
                rec.evaluation_avg_hard_skill = 0.0
                rec.evaluation_avg_communication = 0.0
                rec.evaluation_avg_teamwork = 0.0
                rec.evaluation_avg_total = 0.0
