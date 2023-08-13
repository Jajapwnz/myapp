from PyQt5 import QtCore, QtGui, QtWidgets

class AddDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.code = QtWidgets.QLineEdit()
        self.name = QtWidgets.QLineEdit()
        self.amount = QtWidgets.QSpinBox()
        self.unit = QtWidgets.QLineEdit()
        self.date = QtWidgets.QDateEdit(calendarPopup=True)
        self.expiration = QtWidgets.QDateEdit(calendarPopup=True)  # Добавлено поле для срока годности
        self.document = QtWidgets.QLineEdit()
        self.location = QtWidgets.QLineEdit()
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
        layout.addRow("Срок годности", self.expiration)  # Добавлена строка для срока годности
        layout.addRow("Документ", self.document)
        layout.addRow("Место хранения", self.location)
        layout.addRow("Контакты", self.contacts)
        layout.addRow(buttonBox)

        self.setLayout(layout)

    def accept(self):
        self.code = self.code.text()
        self.name = self.name.text()
        self.amount = self.amount.value()
        self.unit = self.unit.text()
        self.date = self.date.date().toString(QtCore.Qt.ISODate)
        self.expiration = self.expiration.date().toString(QtCore.Qt.ISODate)  # Преобразование даты срока годности
        self.document = self.document.text()
        self.location = self.location.text()
        self.contacts = self.contacts.text()
        super().accept()
