from fastapi import FastAPI
from sql_app import models,schemas,database
from fastapi.staticfiles import StaticFiles
from routers import users,category,inventory


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

models.database.Base.metadata.create_all(database.engine)

app.include_router(users.router)
app.include_router(category.router)
app.include_router(inventory.router)


