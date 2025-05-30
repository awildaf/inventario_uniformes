from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Enum
)
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class EstadoUniforme(enum.Enum):
    nuevo = "nuevo"
    usado = "usado"

class Pais(Base):
    __tablename__ = "paises"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    propiedades = relationship("Propiedad", back_populates="pais")

class Propiedad(Base):
    __tablename__ = "propiedades"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String)
    pais_id = Column(Integer, ForeignKey("paises.id"))
    pais = relationship("Pais", back_populates="propiedades")
    empleados = relationship("Empleado", back_populates="propiedad")

class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False)
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"))
    propiedad = relationship("Propiedad", back_populates="empleados")
    asignaciones = relationship("AsignacionUniforme", back_populates="empleado")

class Uniforme(Base):
    __tablename__ = "uniformes"
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    talla = Column(String, nullable=False)
    estado = Column(Enum(EstadoUniforme), nullable=False)
    descripcion = Column(String)
    existencias = Column(Integer, default=0)
    asignaciones = relationship("AsignacionUniforme", back_populates="uniforme")
    factura_entradas = relationship("FacturaEntrada", back_populates="uniforme")
    factura_salidas = relationship("FacturaSalida", back_populates="uniforme")

class AsignacionUniforme(Base):
    __tablename__ = "asignaciones_uniforme"
    id = Column(Integer, primary_key=True)
    uniforme_id = Column(Integer, ForeignKey("uniformes.id"))
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    fecha_entrega = Column(Date, nullable=False)
    cantidad = Column(Integer, default=1)
    recibo_pdf = Column(String)
    uniforme = relationship("Uniforme", back_populates="asignaciones")
    empleado = relationship("Empleado", back_populates="asignaciones")

class FacturaEntrada(Base):
    __tablename__ = "factura_entradas"
    id = Column(Integer, primary_key=True)
    proveedor = Column(String)
    fecha = Column(Date, nullable=False)
    uniforme_id = Column(Integer, ForeignKey("uniformes.id"))
    cantidad = Column(Integer, nullable=False)
    documento_pdf = Column(String)
    uniforme = relationship("Uniforme", back_populates="factura_entradas")

class FacturaSalida(Base):
    __tablename__ = "factura_salidas"
    id = Column(Integer, primary_key=True)
    motivo = Column(String)
    fecha = Column(Date, nullable=False)
    uniforme_id = Column(Integer, ForeignKey("uniformes.id"))
    cantidad = Column(Integer, nullable=False)
    documento_pdf = Column(String)
    uniforme = relationship("Uniforme", back_populates="factura_salidas")