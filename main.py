#main.py
from PyQt5.QtGui import QColor, QBrush
from PyQt5 import QtCore, QtWidgets

from EditDialog import EditDialog
from interface import Ui_MainWindow
from AddDialog import AddDialog
from ReturnDialog import ReturnDialog
from WarehouseDatabase import WarehouseDatabase
import sys

class WarehouseApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(WarehouseApp, self).__init__()
        self.setupUi(self)

        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_tab1_context_menu)

        self.tableWidget_3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_3.customContextMenuRequested.connect(self.show_tab3_context_menu)

        self.lineEdit.textChanged.connect(self.search_in_tabs)

        self.db = WarehouseDatabase()
        self.load_tab1_data()
        self.load_tab3_data()

    def load_tab1_data(self):
        self.tableWidget.setRowCount(0)

        self.db.cursor.execute('SELECT * FROM tab_1')
        data = self.db.cursor.fetchall()

        current_date = QtCore.QDate.currentDate()

        for row, item in enumerate(data):
            self.tableWidget.insertRow(row)
            for col, value in enumerate(item[1:]):
                table_item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, table_item)

            date_item = self.tableWidget.item(row, 4)
            date = QtCore.QDate.fromString(date_item.text(), "yyyy-MM-dd")

            if date < current_date:
                for col in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(row, col).setBackground(QBrush(QColor(222, 122, 122)))

    def load_tab3_data(self):
        self.tableWidget_3.setRowCount(0)

        self.db.cursor.execute('SELECT * FROM tab_3')
        data = self.db.cursor.fetchall()

        for row, item in enumerate(data):
            self.tableWidget_3.insertRow(row)
            for col, value in enumerate(item[1:]):
                if col not in [6, 7]:  # Exclude columns 6 and 7
                    table_item = QtWidgets.QTableWidgetItem(str(value))
                    self.tableWidget_3.setItem(row, col, table_item)

    def search_in_tabs(self, search_text):
        search_text = search_text.strip().lower()

        self.load_tab1_data()
        self.load_tab3_data()

        if search_text:

            tab1_found = False
            tab3_found = False

            for row in range(self.tableWidget.rowCount()):
                row_visible = False
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    if search_text in item.text().strip().lower():
                        row_visible = True
                        break
                self.tableWidget.setRowHidden(row, not row_visible)
                if row_visible:
                    tab1_found = True

            for row in range(self.tableWidget_3.rowCount()):
                row_visible = False
                for col in range(self.tableWidget_3.columnCount()):
                    item = self.tableWidget_3.item(row, col)
                    if item and search_text in item.text().strip().lower():
                        row_visible = True
                        break
                self.tableWidget_3.setRowHidden(row, not row_visible)
                if row_visible:
                    tab3_found = True

            if tab1_found and self.tabWidget.currentIndex() == 1:
                self.tabWidget.setCurrentIndex(0)
            elif tab3_found and self.tabWidget.currentIndex() == 0:
                self.tabWidget.setCurrentIndex(1)

    def show_tab1_context_menu(self, pos):
        menu = QtWidgets.QMenu()
        addAction = menu.addAction("Добавить")
        returnAction = menu.addAction("Вернуть")
        editAction = menu.addAction("Редактировать")
        deleteAction = menu.addAction("Удалить")

        action = menu.exec_(self.tableWidget.mapToGlobal(pos))

        if action == addAction:
            dialog = AddDialog()
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                code = dialog.code
                name = dialog.name
                amount = dialog.amount
                unit = dialog.unit
                date = dialog.date
                doc = dialog.document
                location = dialog.location
                expiration = dialog.expiration
                contacts = dialog.contacts

                # Insert data into tab_1 table
                self.db.cursor.execute('''
                    INSERT INTO tab_1 (code, name, amount, unit, date, doc, location, expiration, contacts)
                    VALUES (?,?,?,?,?,?,?,?,?)
                ''', (code, name, amount, unit, date, doc, location, expiration, contacts))

                self.db.conn.commit()

                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)

                code_item = QtWidgets.QTableWidgetItem(code)
                name_item = QtWidgets.QTableWidgetItem(name)
                amount_item = QtWidgets.QTableWidgetItem(str(amount))
                unit_item = QtWidgets.QTableWidgetItem(unit)
                date_item = QtWidgets.QTableWidgetItem(date)
                doc_item = QtWidgets.QTableWidgetItem(doc)
                location_item = QtWidgets.QTableWidgetItem(location)
                expiration_item = QtWidgets.QTableWidgetItem(expiration)
                contacts_item = QtWidgets.QTableWidgetItem(contacts)

                self.tableWidget.setItem(row, 0, code_item)
                self.tableWidget.setItem(row, 1, name_item)
                self.tableWidget.setItem(row, 2, amount_item)
                self.tableWidget.setItem(row, 3, unit_item)
                self.tableWidget.setItem(row, 4, date_item)
                self.tableWidget.setItem(row, 5, doc_item)
                self.tableWidget.setItem(row, 6, location_item)
                self.tableWidget.setItem(row, 7, expiration_item)
                self.tableWidget.setItem(row, 8, contacts_item)

        if action == returnAction:
            dialog = ReturnDialog()
            selected_row = self.tableWidget.currentRow()
            selected_data = [self.tableWidget.item(selected_row, col).text() for col in
                             range(self.tableWidget.columnCount())]
            dialog.set_tab1_data(selected_data)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                code = dialog.code
                name = dialog.name
                amount = dialog.amount
                unit = dialog.unit
                date = dialog.date
                doc = dialog.document

                contacts = dialog.contacts

                # Insert data into tab_3 table
                self.db.cursor.execute('''
                                INSERT INTO tab_3 (code, name, amount, unit, date, doc, contacts)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (code, name, amount, unit, date, doc, contacts))

                self.db.conn.commit()

                row = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row)

                code_item = QtWidgets.QTableWidgetItem(code)
                name_item = QtWidgets.QTableWidgetItem(name)
                amount_item = QtWidgets.QTableWidgetItem(str(amount))
                unit_item = QtWidgets.QTableWidgetItem(unit)
                date_item = QtWidgets.QTableWidgetItem(date)
                doc_item = QtWidgets.QTableWidgetItem(doc)

                contacts_item = QtWidgets.QTableWidgetItem(contacts)

                self.tableWidget_3.setItem(row, 0, code_item)
                self.tableWidget_3.setItem(row, 1, name_item)
                self.tableWidget_3.setItem(row, 2, amount_item)
                self.tableWidget_3.setItem(row, 3, unit_item)
                self.tableWidget_3.setItem(row, 4, date_item)
                self.tableWidget_3.setItem(row, 5, doc_item)

                self.tableWidget_3.setItem(row, 8, contacts_item)

                # Subtract the quantity from tab_1
                tab1_row = self.tableWidget.currentRow()
                tab1_amount_item = self.tableWidget.item(tab1_row, 2)
                tab1_amount = int(tab1_amount_item.text())
                subtracted_amount = min(tab1_amount, amount)
                tab1_amount_item.setText(str(tab1_amount - subtracted_amount))

                # Обновление количества в базе данных
                new_amount = tab1_amount - subtracted_amount
                self.db.cursor.execute('''
                                UPDATE tab_1 SET amount = ? WHERE code = ?
                            ''', (new_amount, code))

                self.db.conn.commit()

                # После вычитания количества, проверяем, не стало ли оно равным 0
                if new_amount == 0:
                    # Получаем код товара из выбранной строки
                    code_item = self.tableWidget.item(tab1_row, 0)
                    code = code_item.text()

                    # Удаляем запись из базы данных
                    self.db.cursor.execute('DELETE FROM tab_1 WHERE code = ?', (code,))
                    self.db.conn.commit()

                    # Удаляем строку из таблицы
                    self.tableWidget.removeRow(tab1_row)

        if action == deleteAction:
            row = self.tableWidget.currentRow()
            item = self.tableWidget.item(row, 0)
            code = item.text()

            # Delete data from tab_1 table
            self.db.cursor.execute('DELETE FROM tab_1 WHERE code = ?', (code,))
            self.db.conn.commit()

            self.tableWidget.removeRow(row)

        if action == editAction:
            row = self.tableWidget.currentRow()
            data = [self.tableWidget.item(row, col).text() for col in range(self.tableWidget.columnCount())]
            dialog = EditDialog()
            dialog.set_data(data)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                code = dialog.code
                name = dialog.name
                amount = dialog.amount
                unit = dialog.unit
                date = dialog.date
                doc = dialog.document
                location = dialog.location
                expiration = dialog.expiration
                contacts = dialog.contacts

                # Update data in tab_1 table
                self.db.cursor.execute('''
                    UPDATE tab_1 SET code = ?, name = ?, amount = ?, unit = ?, date = ?, doc = ?, location = ?, expiration = ?, contacts = ?
                    WHERE code = ?
                ''', (code, name, amount, unit, date, doc, location, expiration, contacts,
                      data[0]))  # Use the original code for WHERE clause

                self.db.conn.commit()

                # Update the table widget
                code_item = QtWidgets.QTableWidgetItem(code)
                name_item = QtWidgets.QTableWidgetItem(name)
                amount_item = QtWidgets.QTableWidgetItem(str(amount))
                unit_item = QtWidgets.QTableWidgetItem(unit)
                date_item = QtWidgets.QTableWidgetItem(date)
                doc_item = QtWidgets.QTableWidgetItem(doc)
                location_item = QtWidgets.QTableWidgetItem(location)
                expiration_item = QtWidgets.QTableWidgetItem(expiration)
                contacts_item = QtWidgets.QTableWidgetItem(contacts)

                self.tableWidget.setItem(row, 0, code_item)
                self.tableWidget.setItem(row, 1, name_item)
                self.tableWidget.setItem(row, 2, amount_item)
                self.tableWidget.setItem(row, 3, unit_item)
                self.tableWidget.setItem(row, 4, date_item)
                self.tableWidget.setItem(row, 5, doc_item)
                self.tableWidget.setItem(row, 6, location_item)
                self.tableWidget.setItem(row, 7, expiration_item)
                self.tableWidget.setItem(row, 8, contacts_item)

    def show_tab3_context_menu(self, pos):
        menu = QtWidgets.QMenu()
        editAction = menu.addAction("Редактировать")
        deleteAction = menu.addAction("Удалить")
        action = menu.exec_(self.tableWidget_3.mapToGlobal(pos))

        if action == editAction:
            row = self.tableWidget_3.currentRow()
            data = []
            for col in range(self.tableWidget_3.columnCount()):
                item = self.tableWidget_3.item(row, col)
                if item is not None:
                    data.append(item.text())
                else:
                    data.append("")
            dialog = EditDialog()
            dialog.set_data(data)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                old_code = data[0]  # Get the original code
                new_code = dialog.code
                name = dialog.name
                amount = dialog.amount
                unit = dialog.unit
                date = dialog.date
                doc = dialog.document
                contacts = dialog.contacts

                # Delete the existing row with the old code
                self.db.cursor.execute('DELETE FROM tab_3 WHERE code = ?', (old_code,))
                self.db.conn.commit()

                # Insert a new row with the updated code
                self.db.cursor.execute('''
                    INSERT INTO tab_3 (code, name, amount, unit, date, doc, contacts)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (new_code, name, amount, unit, date, doc, contacts))
                self.db.conn.commit()

                # Update the table widget
                code_item = QtWidgets.QTableWidgetItem(new_code)
                name_item = QtWidgets.QTableWidgetItem(name)
                amount_item = QtWidgets.QTableWidgetItem(str(amount))
                unit_item = QtWidgets.QTableWidgetItem(unit)
                date_item = QtWidgets.QTableWidgetItem(date)
                doc_item = QtWidgets.QTableWidgetItem(doc)
                contacts_item = QtWidgets.QTableWidgetItem(contacts)

                self.tableWidget_3.setItem(row, 0, code_item)
                self.tableWidget_3.setItem(row, 1, name_item)
                self.tableWidget_3.setItem(row, 2, amount_item)
                self.tableWidget_3.setItem(row, 3, unit_item)
                self.tableWidget_3.setItem(row, 4, date_item)
                self.tableWidget_3.setItem(row, 5, doc_item)
                self.tableWidget_3.setItem(row, 8, contacts_item)

        elif action == deleteAction:
            row = self.tableWidget_3.currentRow()
            item = self.tableWidget_3.item(row, 0)
            if item is not None:
                code = item.text()
                # Delete data from tab_3 table
                self.db.cursor.execute('DELETE FROM tab_3 WHERE code = ?', (code,))
                self.db.conn.commit()
                self.tableWidget_3.removeRow(row)

    def closeEvent(self, event):
        # Save the database when the program is closed
        self.db.conn.commit()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec_())