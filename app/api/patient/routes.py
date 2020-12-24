from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from .models import db, Patients, Points
from .schemas import (point_schema, patient_schema)

from sqlalchemy import func

patient = Blueprint(name='patient', import_name=__name__)


@patient.route("/", methods=['GET'])
def get_patients():
    all_patients = Patients.query.all()
    return jsonify(all_patients)


@patient.route('/<int:patientId>', methods=['GET'])
def get_one(patientId):
    current_patient = Patients.get_patient_by_id(id=patientId)
    return jsonify(current_patient)


@patient.route("/create-patient", methods=['POST'])
def create_patient():
    data = request.get_json()
    try:
        data = patient_schema.load(data)
    except ValidationError as err:
        return err.messages, 422

    name, age, sex, ethnicity = data['name'], data['age'], data['sex'], data['ethnicity']

    patient = Patients(
        name=name,
        age=age,
        sex=sex,
        ethnicity=ethnicity,
    )
    db.session.add(patient)
    db.session.commit()

    created_patient = Patients.get_created_patient(
        name=name,
        age=age,
        sex=sex,
        ethnicity=ethnicity)

    return jsonify(created_patient), 201


@patient.route("/enter-points", methods=['POST'])
def enter_points():
    data = request.get_json()

    # todo add validator here
    # try:
    #     data = point_schema.load(data)
    # except ValidationError as err:
    #     return err.messages, 422

    patientId, pointName, coordinateX, coordinateY, coordinateZ = data['patientId'], data[
        'pointName'], data['location']['x'], data['location']['y'], data['location']['z']

    existingPoint = Points.get_point_by_pointName_and_patientId(
        pointName=pointName, patientId=patientId)

    if existingPoint is None:
        point = Points(
            patientId=patientId,
            pointName=pointName,
            coordinateX=coordinateX,
            coordinateY=coordinateY,
            coordinateZ=coordinateZ,
        )
        db.session.add(point)
        db.session.commit()

        patient_point = Points.get_point_by_patientId(patientId=patientId)
        return jsonify(point_schema.dump(patient_point))
    else:
        existingPoint.coordinateX = coordinateX
        existingPoint.coordinateY = coordinateY
        existingPoint.coordinateZ = coordinateZ
        db.session.commit()
        return jsonify(point_schema.dump(existingPoint))


@patient.route('/compare-average/<int:patientId>/<string:pointName>/',
               methods=['GET'])
def compare_average(patientId, pointName):
    comparisonParams = request.args.getlist('comparison')

    this_patient = Patients.get_patient_by_id(patientId)

    patientsFiltered = Patients.get_patients_by_params(
        patient=this_patient, params=comparisonParams)

    patientIds = []
    for _patient in patientsFiltered:
        patientIds.append(_patient.id)

    pointsAvg = db.session.query(
        func.avg(Points.coordinateX).label('coordinateX'),
        func.avg(Points.coordinateY).label('coordinateY'),
        func.avg(Points.coordinateZ).label('coordinateZ')).filter(
        Points.patientId.in_(patientIds),
        Points.pointName == pointName).one()

    patientPoint = Points.get_point_by_patientId(patientId=patientId)
    x = patientPoint.coordinateX - pointsAvg.coordinateX
    y = patientPoint.coordinateY - pointsAvg.coordinateY
    z = patientPoint.coordinateZ - pointsAvg.coordinateZ

    result = {
        pointName: f'{x}, {y}, {z}',
        "Message": f'Your Zygion is {x}mm to the left horizontally, {y}mm higher vertically, and {z}mm lower in depth compared to the average'
    }

    return jsonify(result)
