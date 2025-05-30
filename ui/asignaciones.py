from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QLabel, QComboBox, QSpinBox, QFormLayout, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from sqlalchemy.orm import sessionmaker
from models import AsignacionUniforme, Empleado, Uniforme
from database import engine
from datetime import date

Session = sessionmaker(bind=engine)

class AsignacionForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Asignación")
        self.layout = QFormLayout(self)

        self.empleado = QComboBox()
        self.uniforme = QComboBox()
        self.cantidad = QSpinBox()
        self.cantidad.setMinimum(1)
        self.fecha = QDateEdit(QDate.currentDate())
        self.fecha.setCalendarPopup(True)

        session = Session()
        self.empleados = session.query(Empleado).all()
        for emp in self.empleados:
            self.empleado.addItem(f"{emp.nombre} {emp.apellido} ({emp.propiedad.nombre})", emp.id)

        self.uniformes_map = {}
        uniformes = session.query(Uniforme).filter(Uniforme.existencias > 0).all()
        for uni in uniformes:
            txt = f"{uni.tipo} - Talla: {uni.talla} - Estado: {uni.estado.value} (Stock: {uni.existencias})"
            self.uniforme.addItem(txt, uni.id)
            self.uniformes_map[uni.id] = uni

        session.close()

        self.layout.addRow("Empleado:", self.empleado)
        self.layout.addRow("Uniforme:", self.uniforme)
        self.layout.addRow("Cantidad:", self.cantidad)
        self.layout.addRow("Fecha entrega:", self.fecha)

        btns = QHBoxLayout()
        ok = QPushButton("Guardar")
        cancel = QPushButton("Cancelar")
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        self.layout.addRow(btns)

        self.uniforme.currentIndexChanged.connect(self.update_max_cantidad)
        self.update_max_cantidad()

    def update_max_cantidad(self):
        uni_id = self.uniforme.currentData()
        if uni_id and uni_id in self.uniformes_map:
            disponible = self.uniformes_map[uni_id].existencias
            self.cantidad.setMaximum(disponible if disponible > 0 else 1)
        else:
            self.cantidad.setMaximum(1)

    def get_data(self):
        return {
            "empleado_id": self.empleado.currentData(),
            "uniforme_id": self.uniforme.currentData(),
            "cantidad": self.cantidad.value(),
            "fecha": self.fecha.date().toPyDate()
        }

class AsignacionesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asignación de Uniformes")
        self.resize(800, 400)
        self.layout = QVBoxLayout(self)

        # Tabla
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Empleado", "Uniforme", "Talla", "Estado", "Cantidad", "Fecha"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Nueva asignación")
        btn_layout.addWidget(self.btn_add)
        self.layout.addLayout(btn_layout)

        self.btn_add.clicked.connect(self.add_asignacion)
        self.load_data()

    def load_data(self):
        session = Session()
        asignaciones = session.query(AsignacionUniforme).all()
        self.table.setRowCount(0)
        for asig in asignaciones:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(asig.id)))
            nombre_emp = f"{asig.empleado.nombre} {asig.empleado.apellido}" if asig.empleado else ""
            self.table.setItem(row, 1, QTableWidgetItem(nombre_emp))
            uni_str = asig.uniforme.tipo if asig.uniforme else ""
            self.table.setItem(row, 2, QTableWidgetItem(uni_str))
            self.table.setItem(row, 3, QTableWidgetItem(asig.uniforme.talla if asig.uniforme else ""))
            self.table.setItem(row, 4, QTableWidgetItem(asig.uniforme.estado.value if asig.uniforme else ""))
            self.table.setItem(row, 5, QTableWidgetItem(str(asig.cantidad)))
            self.table.setItem(row, 6, QTableWidgetItem(str(asig.fecha_entrega)))
        session.close()

    def add_asignacion(self):
        form = AsignacionForm(self)
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            session = Session()
            uni = session.query(Uniforme).get(data["uniforme_id"])
            if uni.existencias < data["cantidad"]:
                QMessageBox.warning(self, "Stock insuficiente", "No hay suficientes existencias para realizar la entrega.")
                session.close()
                return
            asig = AsignacionUniforme(
                uniforme_id=data["uniforme_id"],
                empleado_id=data["empleado_id"],
                cantidad=data["cantidad"],
                fecha_entrega=data["fecha"]
            )
            uni.existencias -= data["cantidad"]
            session.add(asig)
            session.commit()
            session.close()
            self.load_data()