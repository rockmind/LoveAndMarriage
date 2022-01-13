import logging
import os

import uvicorn

from fastapi import Depends

from python.services.base_app.base_app import get_current_active_user
from python.services.db_services.love_and_marriage_db import LoveAndMarriageDB
from python.services.models import User
from python.services.base_app import get_base_app

app = get_base_app()


@app.get("/cases/")
async def get_cases(current_user: User = Depends(get_current_active_user), date_from=None, date_to=None):
    logging.info(f"{current_user.user_name}")
    df = await LoveAndMarriageDB.get_cases(date_from, date_to)
    return df.to_json()


@app.get("/provinces/")
async def get_cases(current_user: User = Depends(get_current_active_user), date_from=None, date_to=None):
    logging.info(f"{current_user.user_name}")
    df = await LoveAndMarriageDB.get_provinces(date_from, date_to)
    return df.to_json()


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    uvicorn.run(app, port=8888, debug=True)
