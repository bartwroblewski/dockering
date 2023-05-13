import string
import time

from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from celery import Celery, Task, shared_task
from celery.result import AsyncResult
from mongoengine import Document, fields, connect
import requests

# TODO:
# - deploy somewhere (digital ocean)
# - prod vs dev dockerfiles? (i.e. gunicorn vs flask server)
# - how to debug docker image in VS code?

# - add linting? (i.e. fastapi module is not recognized)

# - is database persistent among builds? - it is , but why does docker compose up result in two instances of Barti person created?
# - czemu tworzy folder node_modules/.vite tez na lokalu, gdy docker compose up?

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis",
        result_backend="redis://redis",
        task_ignore_result=True,
    ),
)
socketio = SocketIO(app)
celery_app = celery_init_app(app)

@shared_task(ignore_result=False)
def long_blocking_process():
    # alphabet = string.ascii_uppercase
    # for letter in alphabet:
    #     Person(name=letter, age=0).save()
    #     time.sleep(5)
    emit('long_process_done', {'data': 42})


connect('dockering', host='mongodb://mongo', username="root", password="example", authentication_source='admin')


class Person(Document):
    name = fields.StringField()
    age = fields.IntField()

for p in Person.objects.all():
    p.delete()
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

@app.route('/long_process')
def long_process():
    result = long_blocking_process.delay()
    return {'result_id': result.id}

@app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }

@app.route('/person')
def person_route():
    return {'person_names': [p.name for p in Person.objects.all()]}

frontend_blueprint = Blueprint(
    'frontend',
    __name__,
    static_url_path='/static/frontend',
)

app.register_blueprint(frontend_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
