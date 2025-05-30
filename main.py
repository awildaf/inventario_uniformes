from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QAction
import sys
from database import init_db
from sample_data import load_sample_data

from ui.uniformes import UniformesWidget
from ui.empleados import EmpleadosWidget
from ui.asignaciones import AsignacionesWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventario de Uniformes")
        self.resize(900, 600)
        self.central = QLabel("Bienvenido al sistema de inventario de uniformes")
        self.setCentralWidget(self.central)

        # Menú
        menubar = self.menuBar()
        gestion = menubar.addMenu("Gestión")
        act_uniformes = QAction("Uniformes", self)
        act_uniformes.triggered.connect(self.show_uniformes)
        gestion.addAction(act_uniformes)
        act_empleados = QAction("Empleados", self)
        act_empleados.triggered.connect(self.show_empleados)
        gestion.addAction(act_empleados)
        act_asignaciones = QAction("Asignaciones", self)
        act_asignaciones.triggered.connect(self.show_asignaciones)
        gestion.addAction(act_asignaciones)

    def show_uniformes(self):
        self.setCentralWidget(UniformesWidget())

    def show_empleados(self):
        self.setCentralWidget(EmpleadosWidget())

    def show_asignaciones(self):
        self.setCentralWidget(AsignacionesWidget())

def main():
    init_db()
    load_sample_data()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()