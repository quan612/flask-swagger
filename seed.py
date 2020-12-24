

from app import create_app, db
from app.api.patient.models import Patients, Points
from faker import Faker

import random

app = create_app()
fake = Faker()

number = 100
fakeEthinicities = ['White', 'Black', 'Asian',
                    'Hispanic', 'Latino', 'American Indian']

fakePointName = [
    'Endocanthi', 'Exocanthi', 'Alar base', 'Chellion', 'Zygion',
    'Infraorbital Margin', 'Supraorbital Notch', 'Labiale Inferius',
    'Labiale Superius', 'Subnasale', 'Supratip', 'Glabella']

# drop tables
db.drop_all()
db.create_all()


def seed_patients():
    fake_users = [Patients(
        name=fake.name(),
        age=random.randint(11, 55),
        sex=random.choice(['Male', 'Female']),
        ethnicity=random.choice(fakeEthinicities),
    ) for i in range(number)]
    db.session.add_all(fake_users)
    db.session.commit()


def seed_points():
    all_patients = Patients.get_all_patients()
    all_ids = [element.id for element in all_patients]
    random.shuffle(all_ids)

    for i in range(number):
        fake_points = Points(
            pointName=random.choice(fakePointName),
            coordinateX=random.randint(0, 20),
            coordinateY=random.randint(0, 20),
            coordinateZ=random.randint(0, 20),
            patientId=all_ids[i]
        )
        db.session.add(fake_points)
    db.session.commit()


seed_patients()
seed_points()
