from fastapi import FastAPI, Request, Response
from jsonrpcserver import Result, Success, dispatch, method
import uvicorn

from src.python.covid_db_api.covid_db_service import CovidDbService

app = FastAPI()

covid_db = CovidDbService()

@method
def ping() -> Result:

    return Success(covid_db.get_cases())


@app.post("/")
async def index(request: Request):
    return Response(dispatch(await request.body()))


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
