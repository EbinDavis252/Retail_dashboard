# utils/auth_config.py

import streamlit_authenticator as stauth
import yaml

def get_authenticator():
    # Sample config — replace with your actual credentials securely
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@example.com',
                    'name': 'Admin',
                    'password': stauth.Hasher(['admin123']).generate()  # hash the password
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'random_signature_key',
            'name': 'retail_dashboard_cookie'
        },
        'preauthorized': {}  # ✅ REMOVE or LEAVE EMPTY for now
    }

    # Create the authenticator object without using the deprecated `preauthorized`
    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

    return authenticator, config
