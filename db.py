from rzd_kpp import db, app
from rzd_kpp.models import User, UserDetails
from rzd_kpp.models import Pass, UserPass
from datetime import date

with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print('Tables created successfully.')
    except Exception as e:
        print(f'Error: {e}')