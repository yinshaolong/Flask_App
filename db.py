from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
#creates an object db which we can use for all tasks requiring the database
    #defining models, queriying from and asving to the database. this object has the base class registed as the base class for orm-related features
    #we could mkae changes to this base class
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class = Base)
