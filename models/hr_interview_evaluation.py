from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrInterviewEvaluation(models.Model):
    """
    Stores the interview evaluation scores for a single applicant per interviewer.
    Enforced so that each interviewer can only submit one evaluation per candidate.
    """
    _name = 'hr.interview.evaluation'
    _description = 'Interview Evaluation'
    _rec_name = 'rater_id'
    _order = 'evaluation_date desc, id desc'

    # ── Relations ───────────────────────────────────────────────────────────
    applicant_id = fields.Many2one(
        comodel_name='hr.applicant',
        string='Applicant',
        required=True,
        ondelete='cascade',
        index=True,
    )
    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job Position',
        related='applicant_id.job_id',
        store=True,
        index=True,
    )
    partner_name = fields.Char(
        string='Candidate Name',
        related='applicant_id.partner_name',
        store=True,
    )

    # ── Scores (0–100, matching the weight percentages) ─────────────────────
    score_personality = fields.Float(
        string='Personality (10%)',
        default=0.0,
        help='Score out of 10 for Personality.',
    )
    score_hard_skill = fields.Float(
        string='Hard Skill (50%)',
        default=0.0,
        help='Score out of 50 for Hard Skills learned from school and past jobs.',
    )
    score_communication = fields.Float(
        string='Communication Skill (30%)',
        default=0.0,
        help='Score out of 30 for Communication Skill.',
    )
    score_teamwork = fields.Float(
        string='Fitness in Team Work (10%)',
        default=0.0,
        help='Score out of 10 for Fitness in Team Work.',
    )

    # ── Computed total ────────────────────────────────────────────────────────
    score_total = fields.Float(
        string='Total',
        compute='_compute_score_total',
        store=True,
        readonly=True,
    )

    # ── Rater info ────────────────────────────────────────────────────────────
    rater_id = fields.Many2one(
        comodel_name='res.users',
        string='Name of Rater',
        default=lambda self: self.env.user,
        required=True,
    )
    recommendations = fields.Text(string='Recommendations')
    evaluation_date = fields.Date(
        string='Date',
        default=fields.Date.today,
    )

    # ── Constraints ───────────────────────────────────────────────────────────
    _sql_constraints = [
        (
            'unique_applicant_rater',
            'UNIQUE(applicant_id, rater_id)',
            'Each interviewer can submit only one evaluation per candidate.',
        ),
    ]

    # ── Compute methods ───────────────────────────────────────────────────────
    @api.depends(
        'score_personality',
        'score_hard_skill',
        'score_communication',
        'score_teamwork',
    )
    def _compute_score_total(self):
        for rec in self:
            rec.score_total = (
                rec.score_personality
                + rec.score_hard_skill
                + rec.score_communication
                + rec.score_teamwork
            )

    # ── Validation ────────────────────────────────────────────────────────────
    @api.constrains(
        'score_personality',
        'score_hard_skill',
        'score_communication',
        'score_teamwork',
    )
    def _check_score_ranges(self):
        limits = {
            'score_personality': ('Personality', 10),
            'score_hard_skill': ('Hard Skill', 50),
            'score_communication': ('Communication Skill', 30),
            'score_teamwork': ('Fitness in Team Work', 10),
        }
        for rec in self:
            for field, (label, max_val) in limits.items():
                val = getattr(rec, field)
                if val < 0 or val > max_val:
                    raise ValidationError(
                        f'{label} score must be between 0 and {max_val}.'
                    )
