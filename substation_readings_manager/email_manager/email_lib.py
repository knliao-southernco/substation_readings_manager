import substation_readings_manager.email_manager.email_manager as em
import configparser

import json


email_manager_primary_receipient_list = [
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

def send_email(filepath):

    receipient_list = email_manager_primary_receipient_list

    email_manager = em.EmailManager()

    for email in receipient_list:
        email_manager.add_primary_recipient(email)

    email_manager.add_text(text="")

    email_manager.add_attachment(filepath)

    #TODO: Need to add something here that refers to which Month
    email_manager.send(subject="MPC Battery Report")
