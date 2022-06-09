from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Instanciate database without having cirvular import issue
db = SQLAlchemy()

class User(db.Model):
    # ! Create users database
    # email, name, hashed_password, confirmed, id
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(60))
    email=db.Column(db.String(50),unique=True,nullable=False)
    password_hash=db.Column(db.String(120),nullable=False)
    confirmed=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime, default =datetime.now)

    def __repr__(self):
        return "User: "+self.email 

class Event(db.Model):
    # ! Create event database
    # id, user_id, start time, duration, platform, invitees[csv], location_link
    id=db.Column(db.Integer,primary_key=True)
    # Create a one to many relationship for the user
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    title=db.Column(db.String(60))
    name=db.Column(db.String(50),nullable=False)
    platform=db.Column(db.String(120),nullable=False)
    invitees=db.Column(db.String(120),nullable=False)
    created_at=db.Column(db.DateTime, default =datetime.now)
    # Relationships
    user = db.relationship('User')

    def __repr__(self):
        return "<Event %r>" % self.id

if __name__ == "__main__":

    # Run this file directly to create the database tables.
    from application import app
    db=SQLAlchemy(app)
    # r = input("Are you sure you would like to drop and delete all the elements of this database? ")
    # db.drop_all() if r == "delete" else print("No tables Dropped")
    # print("Creating database tables...")
    db.create_all()
    print("Done!")