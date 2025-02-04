from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions import *

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'message': 'What you doing'}

@app.get('/pit')
def PIT():
    pit()
    return {'message': 'pit triggered'}

@app.get('/flipper')
def FLIPPER():
    flipper()
    return {'message': 'flipper triggered'}

@app.get('/spinner/')
def SPINNER(onof: bool):
    spinner(onof)
    if onof:
        return {'message': 'spinner on'}
    else:
        return {'message': 'spinner off'}

@app.get('/start')
def STARTMATCH():
    matchtimer()
    return {'message': 'match started'}

@app.get('/stop')
def STOPMATCH():
    stopmatch()
    return {'message': 'match stop flag set'}
