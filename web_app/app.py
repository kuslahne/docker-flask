from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)

    return decorated

@app.route('/')
def index():
    return "Helo World, kus!"

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Your token is valid token for 30 minutes'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'mypassword':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1) }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

# if __name__ == '__main__':
#     app.run(debug=True)
