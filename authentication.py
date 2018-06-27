""" Authentication Generator script for Susi Hardware. Run this script and input options
 to generate a file for using SUSI in authenticated mode
 To run this file use python3 authentication.py <choice_to_be authenticated> <email> <password>
"""
import json_config
import sys

config = json_config.connect('config.json')

def authenticating():
    """Method for setting authentication parameters in the configuration
    :return: None
    """
    try:
        # choice = input('Do you wish to use SUSI in Authenticated Mode? (y/n)\n')
        choice = sys.argv[1]
        print(choice)
        if choice == 'y':
            # email = input('Enter SUSI Sign-in Email Address: ')
            email = sys.argv[2]
            print(email)
            # password = input('Enter SUSI Sign-in Password: ')
            password = sys.argv[3]
            config['usage_mode'] = 'authenticated'
            config['login_credentials']['email'] = email
            config['login_credentials']['password'] = password
        elif choice == 'n':
            print('Setting anonymous mode as default')
            config['usage_mode'] = 'anonymous'
        else:
            raise ValueError
    except ValueError:
        print('Invalid choice. Anonymous mode set as default. Run the configuration script again if you wish '
              'to change your choice.')
        config['usage_mode'] = 'anonymous'

print("Authenticating \n")
authenticating()