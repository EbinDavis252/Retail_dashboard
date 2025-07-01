# utils/auth_config.py

import streamlit_authenticator as stauth

def get_authenticator():
    # ✅ Correct way: use .generate() and access via [0]
    hashed_passwords = stauth.Hasher(['admin123']).generate()

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
            'key': 'abcdef',  # Replace with a secure value
            'name': 'retail_dashboard_cookie'
        }
    }

    # ✅ Instantiate the authenticator
    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

    return authenticator, config
