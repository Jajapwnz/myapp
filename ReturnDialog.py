from PyQt5 import QtCore, QtGui, QtWidgets

class ReturnDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.code = QtWidgets.QLineEdit()
        self.name = QtWidgets.QLineEdit()
        self.amount = QtWidgets.QSpinBox()
        self.unit = QtWidgets.QLineEdit()
        self.date = QtWidgets.QDateEdit(calendarPopup=True)
        self.document = QtWidgets.QLineEdit()
        self.contacts = QtWidgets.QLineEdit()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Код", self.code)
        layout.addRow("Наименование", self.name)
        layout.addRow("Количество", self.amount)
        layout.addRow("Ед. измерения", self.unit)
        layout.addRow("Дата", self.date)
        layout.addRow("Документ", self.document)
        layout.addRow("Контакты", self.contacts)
        layout.addRow(buttonBox)

        self.setLayout(layout)

    def set_tab1_data(self, data):
        self.code.setText(data[0])
        self.name.setText(data[1])
        self.amount.setValue(int(data[2]))
        self.unit.setText(data[3])
        self.date.setDate(QtCore.QDate.fromString(data[4], "yyyy-MM-dd"))
        self.document.setText(data[5])
        self.contacts.setText(data[6])

    def accept(self):
        self.code = self.code.text()
        self.name = self.name.text()
        self.amount = self.amount.value()
        self.unit = self.unit.text()
        self.date = self.date.date().toString(QtCore.Qt.ISODate)
        self.document = self.document.text()
        self.contacts = self.contacts.text()
        super().accept()
