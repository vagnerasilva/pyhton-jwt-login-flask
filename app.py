from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.args.get('token') #http:127.0.0.1:5000/rota?token=sdasdasdqweqfasdasdasdas
        print(token)
        if not token:
            return jsonify({'message': 'Token is invalid'  }),403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is missing or invalid'}),403

        return f(*args, **kwargs)
    return decorated



@app.route('/livre')
def livre():
    return jsonify({'message':'anyone can view this!'}) 

@app.route('/prot')
@token_required
def protegita():
    return '<h1>protegida funcionando</h1>'

@app.route('/login')
def login():
    auth = request.authorization
    print(request.authorization)
    if auth and request.authorization :
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
      #  token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        print("Vc acertou a senha")
      
        return jsonify({'token':token.decode('UTF-8')})
 
    
    return make_response('Could not verify', 401, {'www-Authenticate': 'Basic realm = "Login Required" '})
    
if __name__ == '__main__':
    app.run(debug=True)