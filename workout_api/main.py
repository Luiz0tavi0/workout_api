from fastapi import FastAPI

from workout_api.routers import api_router

app = FastAPI(title='WorkoutApi')


@app.get('/')
async def root():
    return {'message': 'Tomato'}


app.include_router(api_router)
