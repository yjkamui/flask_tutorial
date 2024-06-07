from sqlalchemy import Integer,String,DateTime,Date,Boolean,Text,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime,time,date 
from . import db

# Tables Declarations.

class User(db.Model):
	id:Mapped[int]=mapped_column(Integer,primary_key=True)
	username:Mapped[str]=mapped_column(String(50),nullable=False)
	password:Mapped[str]=mapped_column(String(128),nullable=False)
	email:Mapped[str]=mapped_column(String(128),unique=True,nullable=False)

class Tasks(db.Model):
	id:Mapped[int]=mapped_column(Integer,primary_key=True)
	name:Mapped[str]=mapped_column(String(100),nullable=False)
	create_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)
	due_date:Mapped[date]=mapped_column(Date)
	project_id:Mapped[int]=mapped_column(ForeignKey('projects.id'),nullable=False)
	done:Mapped[Boolean]=mapped_column(Boolean,default=False)

class Projects(db.Model):
	id:Mapped[int]=mapped_column(Integer,primary_key=True)
	name:Mapped[str]=mapped_column(String(100),nullable=False)
	area_id:Mapped[int]=mapped_column(ForeignKey('areas.id'),nullable=False)
	tasks:Mapped[list['Tasks']]=relationship()
	create_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)
	archived:Mapped[Boolean]=mapped_column(Boolean,default=False)

class Areas(db.Model):
	id:Mapped[int]=mapped_column(Integer,primary_key=True)
	name:Mapped[str]=mapped_column(String(100),nullable=False)
	projects:Mapped[list['Projects']]=relationship()
	resources:Mapped[list['Resources']]=relationship()
	create_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)
	archived:Mapped[Boolean]=mapped_column(Boolean,default=False)


class Resources(db.Model):
	id:Mapped[int]=mapped_column(Integer,primary_key=True)
	name:Mapped[str]=mapped_column(String(100),nullable=False)
	area_id:Mapped[int]=mapped_column(ForeignKey('areas.id'),nullable=False)
	project_id:Mapped[int]=mapped_column(ForeignKey('projects.id'),nullable=False)
	uri:Mapped[str]=mapped_column(String(200),nullable=True)
	media_files:Mapped[str]=mapped_column(String(200),nullable=True)
	summary: Mapped[str]=mapped_column(Text,nullable=True)
	create_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)
	archived:Mapped[Boolean]=mapped_column(Boolean,default=False)


