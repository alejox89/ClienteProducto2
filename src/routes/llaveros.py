from fastapi import APIRouter, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from sqlalchemy import text, and_
from models.llavero import llaveros, llaveros2, datosbasicos, datoscomplem, relperproducto
from schemas.llavero_schema import LlaveroSchema, ContenedorResponse, RelperProductoSchema
from fastapi.encoders import jsonable_encoder
import sqlalchemy as dbc
from sqlalchemy.orm import sessionmaker
from config.db2 import DB
from typing import List
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

db = DB.create()
con = db.engine
Session = sessionmaker(bind = con)
session = Session()


llavero = APIRouter()

@llavero.get("/llaverito/mdm/")
async def get_llavemdms(llaveMdm : str):
    return con.execute(llaveros.select().where(llaveros.c.llave_mdm == llaveMdm)).first()

@llavero.get("/llaveritos/mdm/")
async def get_llavemdmsc(llaveMdm : str):
    query = dbc.select([llaveros.columns.llave_mdm, llaveros2.columns.id_persona])
    #query = db.select([llaveros, llaveros2].where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
    query = query.select_from(llaveros.join(llaveros2, llaveros.columns.llave_mdm == llaveros2.columns.id_persona))
    return con.execute(query.select().where(llaveros.c.llave_mdm == llaveMdm)).first()

@llavero.get("/llavero/mdm/")
async def get_llavecif(llavecif : str):
    return con.execute(llaveros.select().where(llaveros.c.llave_cif == llavecif)).first()

@llavero.get("/llaveross/mdm/", response_model=LlaveroSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc(llaveMdm : str):
    try:
        result = con.execute(llaveros.select().where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/datoss/mdm/", response_model=ContenedorResponse, status_code=HTTP_200_OK)
async def get_llavemdmsc(llaveMdm : str):
    try:
        result = session.query(datosbasicos).join(datoscomplem).where(datosbasicos.c.rowid_object == llaveMdm).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/datosss/mdm/", response_model=ContenedorResponse, status_code=HTTP_200_OK)
async def get_llavemdmsc(llaveMdm : str):
    try:
        with con.connect() as conn:
            query = dbc.select([datosbasicos, datoscomplem])
            #query = db.select([llaveros, llaveros2].where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
            query = query.select_from(datosbasicos.join(datoscomplem, datosbasicos.columns.rowid_object == datoscomplem.columns.id_persona))
            result = conn.execute(query.select().where(datosbasicos.c.rowid_object == llaveMdm)).first()
            if result != None:
                return result
            else:
                return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)



@llavero.get("/datos/mdm/")
async def get_llavemdmsc(llaveMdm : str):
    result = session.query(datosbasicos).join(datoscomplem).where(datosbasicos.c.rowid_object == llaveMdm).first()
    #print(result)
    #query = db.select([datosbasicos, datoscomplem])
    #query = db.select([llaveros, llaveros2].where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
    #query = query.select_from(datosbasicos.join(datoscomplem, datosbasicos.columns.rowid_object == datoscomplem.columns.id_persona))
    return result

@llavero.get("/consulta/relperproducto/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc(rowid_object : str):
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == rowid_object).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/consulta/relperproducto/",response_model=List[RelperProductoSchema], status_code=HTTP_200_OK)
async def get_producto(numero_producto : str):
    try:
        result = session.query(relperproducto).where(relperproducto.c.numero_producto == numero_producto).all()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)