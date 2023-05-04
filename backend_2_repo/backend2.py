from fastapi import FastAPI

app = FastAPI()

@app.get('/api/world')
def world_api():
    return 'worlddd'

if __name__ == '__main__':
    #8000
    app.run()