from fastapi import FastAPI
import rsj
from uvicorn import run
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount, Route, Router

app = FastAPI() #openapi_prefix='/f')
# rsj = hug.API(__name__).http.server()

app.mount('/app', WSGIMiddleware(app=rsj.__hug_wsgi__))

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8888, debug=True)
