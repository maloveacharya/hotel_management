{
    'name':'Hotel Management',
    'version':'1.0',
    'summary':'Manage Hotel Booking',
    'sequence':10,
    'description':'Here the all Details of Hotel is available ans Manage the all processes.',
    'category':'hotel management',
    'website':'www.bistasolution.com',
    'depends':['sale_management'],
    'data':[
            'views/hotel.xml',
            'data/ir_sequence_data.xml',
            'wizard/calc_view.xml',

    ],
    'installable': True,
    'application':False,
    'auto_install':False,

}