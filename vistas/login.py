# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaces/login.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1048, 1304)
        Dialog.setStyleSheet("QWidget {\n"
"    background-color: #fdf6e3;\n"
"    font-family: Arial;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 4px;\n"
"    padding: 6px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #008cba;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 6px;\n"
"}\n"
"")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.logo = QtWidgets.QLabel(Dialog)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("interfaces\\logoGestionTapas.jpg"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.verticalLayout.addWidget(self.logo)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.label_rol = QtWidgets.QLabel(Dialog)
        self.label_rol.setObjectName("label_rol")
        self.verticalLayout.addWidget(self.label_rol)
        self.comboRol = QtWidgets.QComboBox(Dialog)
        self.comboRol.setObjectName("comboRol")
        self.comboRol.addItem("")
        self.comboRol.addItem("")
        self.comboRol.addItem("")
        self.verticalLayout.addWidget(self.comboRol)
        self.btnLogin = QtWidgets.QPushButton(Dialog)
        self.btnLogin.setObjectName("btnLogin")
        self.verticalLayout.addWidget(self.btnLogin)
        self.botonRegistro = QtWidgets.QPushButton(Dialog)
        self.botonRegistro.setObjectName("botonRegistro")
        self.verticalLayout.addWidget(self.botonRegistro)
        self.botonAnonimo = QtWidgets.QPushButton(Dialog)
        self.botonAnonimo.setObjectName("botonAnonimo")
        self.verticalLayout.addWidget(self.botonAnonimo)
        self.labelError = QtWidgets.QLabel(Dialog)
        self.labelError.setStyleSheet("color: red;\n"
"font-weight: bold;")
        self.labelError.setText("")
        self.labelError.setObjectName("labelError")
        self.verticalLayout.addWidget(self.labelError)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Introduce tu email"))
        self.label_2.setText(_translate("Dialog", "Introduce tu contraseña"))
        self.label_rol.setText(_translate("Dialog", "Selecciona tu rol"))
        self.comboRol.setItemText(0, _translate("Dialog", "Cliente"))
        self.comboRol.setItemText(1, _translate("Dialog", "Empleado"))
        self.comboRol.setItemText(2, _translate("Dialog", "Administrador"))
        self.btnLogin.setText(_translate("Dialog", "Iniciar sesión"))
        self.botonRegistro.setText(_translate("Dialog", "Registrarse"))
        self.botonAnonimo.setText(_translate("Dialog", "Entrar como invitado"))
