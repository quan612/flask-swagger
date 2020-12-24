from .models import Points, Patients
from marshmallow import fields
from app import ma


class PointsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Points
        # fields = ("patientId", "pointName", "coordinate")

    coordinate = fields.Method("get_coordinate")

    def get_coordinate(self, obj):
        return str(obj.coordinateX) + ',' + str(obj.coordinateY) + ',' + str(obj.coordinateZ)


point_schema = PointsSchema()


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patients
        # fields = ("id", "age", "sex", "ethnicity")


patient_schema = PatientSchema()
