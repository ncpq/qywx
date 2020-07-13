from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


engine = create_engine('mysql://pig:2020@bali@222.203.0.6:3360/qywx')
session = engine.connect()