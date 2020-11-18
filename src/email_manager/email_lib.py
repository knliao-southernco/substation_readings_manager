import src.email_manager.email_manager as em

test_primary_receipient_list = [
        'knliao@southernco.com'
    ]


primary_receipient_list = [
    'jrstewar@southernco.com',
    'EBBRAY@southernco.com',
    'JONJAMES@southernco.com',
    'RJSCHNEI@southernco.com', 
    'BCYOUMAN@southernco.com',
    'CALITTON@southernco.com',
    'TFETTERL@southernco.com'
]

def send_email(filepath='../October2020 MPC Battery Report.xlsx'): 

    test = em.EmailManager()

    for email in test_primary_receipient_list:
        test.add_primary_recipient(email)
    
    test.add_text(text="")

    test.add_attachment(filepath)
    test.send(subject="MPC Battery Report")
