from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QLabel, QLineEdit, QComboBox, QSpinBox, QFormLayout
)
from PyQt5.QtCore import Qt
from sqlalchemy.orm import sessionmaker
from models import Uniforme, EstadoUniforme
from database import engine

Session = sessionmaker(bind=engine)

class UniformeForm(QDialog):
    def __init__(self, parent=None, uniforme=None):
        super().__init__(parent)
        self.setWindowTitle("Uniforme")
        self.uniforme = uniforme
        self.layout = QFormLayout(self)

        self.tipo = QLineEdit()
        self.talla = QLineEdit()
        self.estado = QComboBox()
        self.estado.addItems([e.value for e in EstadoUniforme])
        self.descripcion = QLineEdit()
        self.existencias = QSpinBox()
        self.existencias.setMaximum(9999)

        self.layout.addRow("Tipo:", self.tipo)
        self.layout.addRow("Talla:", self.talla)
        self.layout.addRow("Estado:", self.estado)
        self.layout.addRow("Descripción:", self.descripcion)
        self.layout.addRow("Existencias:", self.existencias)

        btns = QHBoxLayout()
        ok = QPushButton("Guardar")
        cancel = QPushButton("Cancelar")
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        self.layout.addRow(btns)

        if uniforme:
            self.tipo.setText(uniforme.tipo)
            self.talla.setText(uniforme.talla)
            self.estado.setCurrentText(uniforme.estado.value)
            self.descripcion.setText(uniforme.descripcion or "")
            self.existencias.setValue(uniforme.existencias)

    def get_data(self):
        return {
            "tipo": self.tipo.text(),
            "talla": self.talla.text(),
            "estado": self.estado.currentText(),
            "descripcion": self.descripcion.text(),
            "existencias": self.existencias.value()
        }

class UniformesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Uniformes")
        self.resize(700, 400)
        self.layout = QVBoxLayout(self)

        # Tabla
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Tipo", "Talla", "Estado", "Existencias"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Agregar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Eliminar")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        self.layout.addLayout(btn_layout)

        # Evento
        self.btn_add.clicked.connect(self.add_uniforme)
        self.btn_edit.clicked.connect(self.edit_uniforme)
        self.btn_delete.clicked.connect(self.delete_uniforme)

        self.load_data()

    def load_data(self):
        session = Session()
        uniformes = session.query(Uniforme).all()
        self.table.setRowCount(0)
        for uni in uniformes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(uni.id)))
            self.table.setItem(row, 1, QTableWidgetItem(uni.tipo))
            self.table.setItem(row, 2, QTableWidgetItem(uni.talla))
            self.table.setItem(row, 3, QTableWidgetItem(uni.estado.value))
            self.table.setItem(row, 4, QTableWidgetItem(str(uni.existencias)))
        session.close()

    def add_uniforme(self):
        form = UniformeForm(self)
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            session = Session()
            uni = Uniforme(
                tipo=data["tipo"],
                talla=data["talla"],
                estado=EstadoUniforme(data["estado"]),
                descripcion=data["descripcion"],
                existencias=data["existencias"]
            )
            session.add(uni)
            session.commit()
            session.close()
            self.load_data()

    def edit_uniforme(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Editar", "Seleccione un uniforme para editar.")
            return
        uni_id = int(self.table.item(selected, 0).text())
        session = Session()
        uni = session.query(Uniforme).get(uni_id)
        form = UniformeForm(self, uni)
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            uni.tipo = data["tipo"]
            uni.talla = data["talla"]
            uni.estado = EstadoUniforme(data["estado"])
            uni.descripcion = data["descripcion"]
            uni.existencias = data["existencias"]
            session.commit()
            session.close()
            self.load_data()
        else:
            session.close()

    def delete_uniforme(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Eliminar", "Seleccione un uniforme para eliminar.")
            return
        uni_id = int(self.table.item(selected, 0).text())
        session = Session()
        uni = session.query(Uniforme).get(uni_id)
        confirm = QMessageBox.question(self, "Eliminar", f"¿Eliminar uniforme '{uni.tipo} {uni.talla}'?")
        if confirm == QMessageBox.Yes:
            session.delete(uni)
            session.commit()
            session.close()
            self.load_data()
        else:
            session.close()