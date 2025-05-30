from database import SessionLocal, init_db
from models import Pais, Propiedad, Empleado, Uniforme, EstadoUniforme
from datetime import date

def load_sample_data():
    session = SessionLocal()
    if session.query(Pais).first():
        print("Datos de prueba ya insertados.")
        session.close()
        return

    rd = Pais(nombre="Rep Dominicana")
    mx = Pais(nombre="México")
    session.add_all([rd, mx])
    session.commit()

    hotel1 = Propiedad(nombre="Hotel Sol Caribe", direccion="Av. Malecón, Santo Domingo", pais=rd)
    hotel2 = Propiedad(nombre="Hotel Playa Azul", direccion="Playa Bávaro, Punta Cana", pais=rd)
    hotel3 = Propiedad(nombre="Hotel Costa Verde", direccion="Zona Hotelera, Cancún", pais=mx)
    session.add_all([hotel1, hotel2, hotel3])
    session.commit()

    emp1 = Empleado(nombre="Juan", apellido="Pérez", documento="001-1234567-8", propiedad=hotel1)
    emp2 = Empleado(nombre="Ana", apellido="Gómez", documento="002-7654321-9", propiedad=hotel2)
    session.add_all([emp1, emp2])
    session.commit()

    u1 = Uniforme(tipo="Camisa", talla="M", estado=EstadoUniforme.nuevo, existencias=50, descripcion="Camisa blanca manga corta")
    u2 = Uniforme(tipo="Pantalón", talla="L", estado=EstadoUniforme.nuevo, existencias=40, descripcion="Pantalón negro")
    u3 = Uniforme(tipo="Zapatos", talla="40", estado=EstadoUniforme.nuevo, existencias=30, descripcion="Zapatos negros formal")
    u4 = Uniforme(tipo="Camisa", talla="M", estado=EstadoUniforme.usado, existencias=10, descripcion="Camisa blanca usada")
    session.add_all([u1, u2, u3, u4])
    session.commit()

    session.close()
    print("Datos de prueba insertados exitosamente.")

if __name__ == "__main__":
    init_db()
    load_sample_data()