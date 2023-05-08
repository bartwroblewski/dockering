from flask import Flask, render_template, Blueprint
from mongoengine import Document, fields, connect
import requests

# TODO:
# - add some static files like images, JS, css
# - play with ports in Flask and Fastapi too see the relationship with dockerfile/dockercompose
# - add linting? (i.e. fastapi module is not recognized)
# - how to debug docker image in VS code?
# - prod vs dev dockerfiles? (i.e. gunicorn vs flask server)
# - for prod, remove Vite dependency and add NGINX for serving the static build
# - is database persistent among builds?
# - czemu tworzy folder node_modules/.vite na lokalu, gdy docker compose up?


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

frontend_blueprint = Blueprint('frontend', __name__, root_path="frontend", template_folder="templates")

@frontend_blueprint.route('/')
def index():
    return render_template('frontend/index.html')

app.register_blueprint(frontend_blueprint)

if __name__ == '__main__':
    #5000
    app.run(debug=True, host='0.0.0.0')
