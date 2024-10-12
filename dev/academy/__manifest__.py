{
    'name': 'Academy',
    'version': '17.0.1.0.0',

    'summary': 'Module for managing an academy',
    'description': """
        This module helps in managing an academy, including courses, students, and instructors.
    """,
    'author': 'oqdevpy',
    'website': 'https://www.oqdev.uz',
    'category': 'Education',
    'depends': ['base', 'web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',   
        'views/education_group_view.xml',
        'views/employee_views.xml',   
        # 'views/user_inherit.xml',   
        'views/education_student_view.xml',
        'views/education_teacher_view.xml',
        'views/education_course_view.xml',
        'views/education_payment_view.xml',
        'views/education_payout_view.xml',
         
    ],
    'demo': [
        # List of demo files, e.g., 'demo/academy_demo.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}