import re
import random
import string
from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='User Registration API', description='API for user registration and email confirmation')

ns = api.namespace('register', description='User Registration')

registration_model = api.model('Registration', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'confirm_password': fields.String(required=True, description='Confirm password'),
})

registered_users = []

registration_requests = {}

email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def generate_confirmation_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

@ns.route('')
class UserRegistration(Resource):
    @ns.expect(registration_model)
    def post(self):
        """
        Request user registration
        """
        data = request.json
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        if not re.match(email_regex, email):
            return {'message': 'Invalid email address format'}, 400

        if email in [user['email'] for user in registered_users]:
            return {'message': 'Email already registered'}, 400

        if email in registration_requests:
            return {'message': 'Email already requested for registration'}, 400

        if password != confirm_password:
            return {'message': 'Passwords do not match'}, 400

        confirmation_token = generate_confirmation_token()

        registration_requests[confirmation_token] = {
            'email': email,
            'password': password,
        }

        confirmation_link = f"http://localhost:5000/confirm/{confirmation_token}"

        return {
            'message': 'Registration request received',
            'confirmation_link': confirmation_link
        }, 201

@ns.route('/registered')
class RegisteredUsers(Resource):
    def get(self):
        """
        Get all registered users
        """
        return {'registered_users': registered_users}

@app.route('/confirm/<string:confirmation_token>', methods=['GET'])
def confirm_email(confirmation_token):
    """
    Confirm user registration
    """
    if confirmation_token in registration_requests:
        user_data = registration_requests[confirmation_token]
        del registration_requests[confirmation_token]
        
        registered_users.append(user_data)

        return f'Email confirmed. You are now registered!'
    else:
        return 'Invalid confirmation token', 404

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
