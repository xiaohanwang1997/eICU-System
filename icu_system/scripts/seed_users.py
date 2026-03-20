from app import create_app
from app.extensions import db
from app.models import User


app = create_app()

with app.app_context():
    doctor = User.query.filter_by(username='doctor1').first()
    admin = User.query.filter_by(username='admin1').first()

    if not doctor:
        doctor = User(username='doctor1', role='doctor')
        doctor.set_password('password123')
        db.session.add(doctor)

    if not admin:
        admin = User(username='admin1', role='admin')
        admin.set_password('password123')
        db.session.add(admin)

    db.session.commit()
    print('Users seeded successfully.')
