from app import app
from db import db

db.init_app(app)

#before the first request runs(any request), this code runs to create data.db file
@app.before_first_request#flask decorator
def create_tables():
    db.create_all()
