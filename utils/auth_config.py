# utils/auth_config.py

import streamlit_authenticator as stauth

def get_authenticator():
    # ✅ Correct way: hash the password using a list and extract directly
    hashed_passwords = stauth.Hasher().hash(['admin123'])

    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@example.com',
                    'name': 'Admin',
                    'password': hashed_passwords[0]  # ✅ Correct access
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'abcdef',  # Change to a secure secret in production
            'name': 'retail_dashboard_cookie'
        }
    }

    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

    return authenticator, config
