# utils/auth_config.py

import streamlit_authenticator as stauth

def get_authenticator():
    # ✅ Correct way to hash passwords safely
    passwords = ['admin123']
    hasher = stauth.Hasher(passwords)
    hashed_passwords = hasher.generate()  # Will be a dictionary: { 'admin123': hashed_val }

    # Extract hashed value directly from dict using password string
    admin_password_hashed = hashed_passwords['admin123']

    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'name': 'Admin',
                    'password': admin_password_hashed,
                    'email': 'admin@example.com'
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'abcdef',  # Use a strong random key in production
            'name': 'retail_dashboard_cookie'
        }
    }

    # Create authenticator instance
    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

    return authenticator, config
