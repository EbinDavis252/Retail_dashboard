# utils/auth_config.py

import streamlit_authenticator as stauth

def get_authenticator():
    # Hashing the password correctly
    hashed_passwords = stauth.Hasher().hash(['admin123'])

    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'name': 'Admin',
                    'password': hashed_passwords[0],
                    'email': 'admin@example.com'
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'abcdef',  # Use a secure random string in production
            'name': 'retail_dashboard_cookie'
        }
    }

    # Initialize the authenticator
    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

    return authenticator, config
