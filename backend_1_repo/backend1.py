from flask import Flask, Blueprint

app = Flask(__name__)

@app.route('/echo')
def echo():
    return {'data': 'hi there'}

frontend_blueprint = Blueprint(
    'frontend',
    __name__,
    static_url_path='/static/frontend',
)

app.register_blueprint(frontend_blueprint)

if __name__ == '__main__':
    app.run(app, host='0.0.0.0')
