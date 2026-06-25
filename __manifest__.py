{
    'name': 'HR Interview Evaluation Form',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Recruitment',
    'summary': 'Adds a structured interview evaluation form to recruitment applicants and job positions.',
    'description': """
        Adds a per-applicant interview evaluation tab (Personality, Hard Skill,
        Communication, Teamwork) to hr.applicant, and a consolidated comparison
        table on the hr.job (Job Position) form showing all evaluated candidates.
    """,
    'author': 'Top System Solution and Technology',
    'depends': ['hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_interview_evaluation_views.xml',
        'views/hr_applicant_views.xml',
        'views/hr_job_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_interview_evaluation/static/src/css/interview_form.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
