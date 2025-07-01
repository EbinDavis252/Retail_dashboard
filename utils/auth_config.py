pip install streamlit-authenticator==0.2.2
# utils/auth_config.py

import streamlit_authenticator as stauth

def get_authenticator():
    # ✅ Hash password using version-compatible method
    hashed_passwords = stauth.Hasher(['admin123']).generate()  # returns a list

    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'name': 'Admin',
                    'password': hashed_passwords[0],  # Access first hashed password
                    'email': 'admin@example.com'
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'abcdef',  # Secure key
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
