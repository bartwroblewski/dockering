from flask import Flask, url_for, send_from_directory, Blueprint
from mongoengine import Document, fields, connect
import requests

# TODO:
# - nie moze byc 2 roznych buildow frontendu (dla backendu1 i nginxa), bo bede rozne hashe assetow, i zawsze bedzie skrypt/css not found przez nginxa
# - for prod, remove Vite dependency and add NGINX for serving the static build
# - prod vs dev dockerfiles? (i.e. gunicorn vs flask server)
# - how to debug docker image in VS code?

# - add some static files like images, JS, css
# - add linting? (i.e. fastapi module is not recognized)

# - is database persistent among builds? - it is , but why does docker compose up result in two instances of Barti person created?
# - czemu tworzy folder node_modules/.vite tez na lokalu, gdy docker compose up?


app = Flask(__name__)
connect('dockering', host='mongodb://mongo', username="root", password="example", authentication_source='admin')


class Person(Document):
    name = fields.StringField()
    age = fields.IntField()

person = Person(name='Barti', age=100)
person.save()

class WorldService:
    def get(self):
        response = requests.get('http://backend2:8000/api/world')
        return response.json()
    
world_service = WorldService()

@app.route('/api/hello', methods=['GET'])
def hello_api():
    world = world_service.get()
    person = Person.objects.first()
    return f'hellooo {world}, person: {person.name}'

@app.route('/echo')
def echo():
    return {'data': 'hi there'}

frontend_blueprint = Blueprint(
    'frontend',
    __name__,
    root_path="frontend",
    template_folder="static",
    static_folder="static",
    static_url_path='/static/frontend',
)

# @frontend_blueprint.route('/')
# def index():
#     return app.send_static_file('index.html')

app.register_blueprint(frontend_blueprint)

if __name__ == '__main__':
    #5000
    app.run(debug=True, host='0.0.0.0')
