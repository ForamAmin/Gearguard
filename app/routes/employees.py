# app/routes/employee.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


# 1) post request : employee sending maintainenece request 




#2) get request : get all maintenance requests of an employee with id 


