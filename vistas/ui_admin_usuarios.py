from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AdminUsuarios(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(695, 340)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tablaUsuarios = QtWidgets.QTableWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tablaUsuarios.setFont(font)
        self.tablaUsuarios.setColumnCount(4)
        self.tablaUsuarios.setRowCount(0)
        self.tablaUsuarios.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Rol"])
        self.verticalLayout.addWidget(self.tablaUsuarios)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)

        self.Rol = QtWidgets.QComboBox(self.groupBox)
        self.Rol.setFont(QtGui.QFont("", 9, QtGui.QFont.Bold))
        self.Rol.addItems(["cliente", "empleado", "administrador"])
        self.horizontalLayout.addWidget(self.Rol)

        self.btnActualizar = QtWidgets.QPushButton(self.groupBox)
        self.btnActualizar.setFont(QtGui.QFont("", 9, QtGui.QFont.Bold))
        self.btnActualizar.setObjectName("btnActualizar")
        self.btnActualizar.setText("Actualizar")
        self.horizontalLayout.addWidget(self.btnActualizar)

        self.btnAbrirCrearUsuario = QtWidgets.QPushButton(self.groupBox)
        self.btnAbrirCrearUsuario.setFont(QtGui.QFont("", 9, QtGui.QFont.Bold))
        self.btnAbrirCrearUsuario.setObjectName("btnAbrirCrearUsuario")
        self.btnAbrirCrearUsuario.setText("Añadir")
        self.horizontalLayout.addWidget(self.btnAbrirCrearUsuario)

        self.Eliminar = QtWidgets.QPushButton(self.groupBox)
        self.Eliminar.setFont(QtGui.QFont("", 9, QtGui.QFont.Bold))
        self.Eliminar.setObjectName("Eliminar")
        self.Eliminar.setText("Eliminar")
        self.horizontalLayout.addWidget(self.Eliminar)

        self.verticalLayout.addWidget(self.groupBox)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
