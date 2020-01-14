#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mess import Request, Response, Router, NotFound
from wsgiref.simple_server import make_server
from db import MedicDB

PASSWORD = 'password123'

def patients(request):
    # Get all patients from db
    medicdb = MedicDB(PASSWORD)

    response = """<h2>All Patients</h2>
                <ul>"""
    try:
        patients = medicdb.get_all_from_table('Patients')
        for patient in patients:
            response += f'<a href="/patients?id={patient.patient_id}"><li>{patient.surname} {patient.name} {patient.patronymic}</li></a>'
        response += '</ul>'
    except NotFound:
        response = "<h3>No Patients</h3>"
    
    # Render patient page
    patient_id = request.args.get('id')
    if patient_id is not None:
        response = """
                    <h2>Patient information</h2>
                   """
        try:
            patient = medicdb.get_patient_by_id(int(patient_id))
            response += f'''<p>
                                <b>{patient.name} {patient.surname}</b>
                                <b>{patient.patronymic}</b>
                            </p>
                            <p>
                            <span>System ID</span>
                            <span>{patient.patient_id}</span>
                            </p>
                            
                        '''
        except NotFound:
            response = "<h3>You are looking for wrong patient!</h3>"

    return Response(response)

def doctors(request):
    medicdb = MedicDB(PASSWORD)
    response = """<h2>All Doctors</h2>
                <ul>"""
    try:
        doctors = medicdb.get_all_from_table('Doctors')
        for doctor in doctors:
            response += f'<a href="/doctors?id={doctor.doctor_id}"><li>{doctor.surname} {doctor.name} {doctor.patronymic}</li></a>'
        response += '</ul>'
    except NotFound:
        response = "<h3>No Doctors!</h3>"
    # Render patient page
    doctor_id = request.args.get('id')
    if doctor_id is not None:
        response = """
                    <h2>Doctor information</h2>
                   """
        try:
            doctor = medicdb.get_doctor_by_id(int(doctor_id))
            response += f'''<p>
                                <b>{doctor.name} {doctor.surname}</b>
                                <b>{doctor.patronymic}</b>
                            </p>
                            <p>
                            <span>System ID</span>
                            <span>{doctor.doctor_id}</span>
                            </p>
                            
                        '''
        except NotFound:
            response = "<h3>You are looking for wrong doctor!</h3>"

    return Response(response)


# Adding routes
routes = Router()

routes.add_route('/patients', patients)
routes.add_route('/', patients)

routes.add_route('/doctors', doctors)

# entry point to WSGI app
def app(environ, start_response):
    try:
        request = Request(environ)
        callback = routes.match(request.path)
        response = callback(request)
    except NotFound:
        response = Response("<h1>Not Found</h1>", status=404)

    start_response(response.status, response.headers.items())
    return iter(response)
    
if __name__ == '__main__':
    port = 8000
    host = 'localhost'
    with make_server(host, port, app) as server:
        print(f"Serving on host: {host} at port: {port}")
        server.serve_forever()