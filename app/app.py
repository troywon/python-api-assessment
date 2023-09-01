from flask import Flask, request
from flask_restx import Api, Resource, fields
import random
import string

app = Flask(__name__)
api = Api(app, version='1.0', title='User Registration API', description='API for user registrration and email confirmation')

ns = api.namespace('register', description='User Registration')

registration_model = api.model('Registration', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'confirm_password': fields.String(required=True, description='Confirm password'),
})

registered_users = {}

def generate_confirmation_link():
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return f"http://localhost/confirm?token={random_chars}"

@ns.route('')
class UserRegistration(Resource):
    @ns.expect(registration_model)
    def post(self):
        data = request.json
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        
        if email in registered_users:
            return {'message': 'Email already registered'}, 400
        
        if password != confirm_password:
            return {'messsage', 'Passwords do not match'}, 400
        
        confirmation_link = generate_confirmation_link
        
        registered_users[email] = {
            'email': email,
            'password': password,
            'confirmed': False,
            'confirmation_link': confirmation_link
        }
        
        return {
            'message': 'User Registered successfully',
            'confirmation_link' : confirmation_link
        }, 201
        
if __name__ == '__main__':
    app.run(debug=True)