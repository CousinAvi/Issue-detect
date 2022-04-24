import asyncio
import json
import multiprocessing
from typing import List

import aiogram
import uvicorn
from aiogram import types, Dispatcher, Bot
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import aiogram.utils.markdown

from .db import engine, get_db
from .db import models as models

from . import schemas

from .db_renewer import Renewer
from .bot import bot, dp
from . import checker

renewer = Renewer()

app = FastAPI(redoc_url="/api/redoc")
models.Base.metadata.create_all(bind=engine)

WEBHOOK_PATH = f"/bot/5173732024:AAFY-kMYgBySve6ILTpsY2LEnwtbeuPoKtQ"
WEBHOOK_URL = "https://detect.site" + WEBHOOK_PATH


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)


@app.post(WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.get_session().close()


@app.get("/api/v1/initiate_portals_parsing")
async def find_all_portals(db=Depends(get_db)):
    multiprocessing.Process(target=renewer.run).start()
    return JSONResponse(
        status_code=200, content={"detail": "Database renewal initiated"}
    )


@app.get("/api/v1/dp_update_status")
async def get_status():
    return JSONResponse(content={"status": renewer.currently_run.value})


@app.get("/api/v1/get_orgs", response_model=List[schemas.Organization])
async def get_orgs(db: Session = Depends(get_db)):
    return db.query(models.OrganizationWithPortals).all()


@app.post("/api/v1/ml_event")
async def get_ml_event(event: schemas.MlEvent, db: Session = Depends(get_db)):
    newEvent = models.MlEvent(**event.dict())
    db.add(newEvent)
    db.flush()
    db.refresh(newEvent)

    message_text = f"""
{aiogram.utils.markdown.bold('Hashtag')}
#event{newEvent.id}\n
{aiogram.utils.markdown.bold('Компания')}:
{event.company}\n
{aiogram.utils.markdown.bold('Сервис')}:
{event.service}\n
{aiogram.utils.markdown.bold('Причина')}:
{event.reason}\n
{aiogram.utils.markdown.bold('Коммент')}:
{event.comment}
    """

    message = await bot.send_message(
        -661257758, message_text + "\nПроверка...", parse_mode="Markdown"
    )

    bank: models.OrganizationWithPortals = (
        db.query(models.OrganizationWithPortals)
        .filter(models.Organization.name.ilike(f"%{event.company}%"))
        .first()
    )

    if bank is not None:
        infos = []

        for portal in bank.portals:
            infos.extend(checker.main(portal.address, bank.name, bank.reg_number))

        resulting_text = message_text + "\n"

        for info_ind in range(len(infos)):
            resulting_text += aiogram.utils.markdown.code(f"{info_ind+1}:\n")
            resulting_text += aiogram.utils.markdown.bold("Сервис: ")
            resulting_text += infos[info_ind]["service"] + "\n\n"
            resulting_text += (
                aiogram.utils.markdown.code(infos[info_ind]["issue"]) + "\n\n"
            )

        await bot.edit_message_text(
            resulting_text, message.chat.id, message.message_id, parse_mode="Markdown"
        )
    else:
        await bot.edit_message_text(
            message_text, message.chat.id, message.message_id, parse_mode="Markdown"
        )


@app.get("/api/v1/test_message")
async def test():
    await bot.send_message(-661257758, "Test Message")


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=80, log_level="info")
