
from app import db
# from marshmallow import fields
from dataclasses import dataclass


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


@dataclass
class Points(db.Model):
    """Data model for Point."""

    __tablename__ = 'Points'

    id = db.Column(db.Integer, primary_key=True)
    pointName = db.Column(
        db.String(20),
        nullable=False
    )
    coordinateX = db.Column(
        db.Integer,
        nullable=False
    )
    coordinateY = db.Column(
        db.Integer,
        nullable=False
    )
    coordinateZ = db.Column(
        db.Integer,
        nullable=False
    )

    patientId = db.Column(
        db.Integer,
        db.ForeignKey('Patients.id'),
        nullable=False
    )

    id: int
    pointName: str
    coordinateX: int
    coordinateY: str
    coordinateZ: str
    patientId: int

    def __repr__(self):
        return '<Points {}>'.format(self.id)

    def get_point_by_patientId(patientId):
        return Points.query.filter(patientId == Points.patientId).first()

    def get_point_by_pointName_and_patientId(pointName, patientId):
        return Points.query.filter(
            pointName == Points.pointName, patientId
            == Points.patientId).first()


@dataclass
class Patients(db.Model):
    """Data model for patient."""

    __tablename__ = 'Patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(50),
        nullable=False
    )
    age = db.Column(
        db.Integer,
        nullable=False
    )
    sex = db.Column(
        db.String(20),
        nullable=False
    )
    ethnicity = db.Column(
        db.String(30),
        nullable=False
    )
    points = db.relationship(
        'Points',
        backref='patient',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        uselist=False
    )

    id: int
    name: str
    age: int
    sex: str
    ethnicity: str
    points: Points

    def __repr__(self):
        return '<Patient {}>'.format(self.id)

    def get_all_patients():
        return Patients.query.all()

    def get_patient_by_id(id):
        return Patients.query.filter(Patients.id == id).first()

    def get_created_patient(name, age, sex, ethnicity):
        return Patients.query.filter(
            Patients.name == name, Patients.age == age, Patients.sex == sex,
            Patients.ethnicity == ethnicity).order_by(
            Patients.id.desc()).first()

    def get_patients_by_params(patient, params):
        filterArr = [Patients.id != patient.id]

        if 'Sex' in params:
            filterArr.append(Patients.sex == patient.sex)

        if 'Ethnicity' in params:
            filterArr.append(Patients.ethnicity == patient.ethnicity)

        return db.session.query(Patients)\
            .filter(*filterArr)
