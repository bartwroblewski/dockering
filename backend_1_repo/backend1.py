from flask import Flask
from mongoengine import Document, fields, connect
import requests

# TODO:
# - add some static files like images, JS, css
# - play with ports in Flask and Fastapi too see the relationship with dockerfile/dockercompose
# - how to debug docker image in VS code?


app = Flask(__name__)
connect('dockering', host='mongodb://mongo', username="root", password="example", authentication_source='admin')

class Person(Document):
    name = fields.StringField()
    age = fields.IntField()

person = Person(name='Barti', age=100)
person.save()

# startup_person = Person(name='Startup person name', age=99)

# so database needs to run before the app
# startup_person.save()

# should be other repo and app
class WorldService:
    def get(self):
        # raise
        # return 'world'
        response = requests.get('http://backend2:8000/api/world')
        return response.json()
    
world_service = WorldService()

@app.route('/api/hello', methods=['GET'])
def hello_api():
    world = world_service.get()
    person = Person.objects.first()
    return f'hellooo {world}, person: {person.name}'

if __name__ == '__main__':
    #5000
    app.run(debug=True, host='0.0.0.0')
