import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import *


class AddForm(QDialog):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('add_order.ui', self)
        self.id_staff = args[0]
        self.accept_btn.clicked.connect(self.add_order)
        self.orders_table = args[1]

    def add_order(self):
        try:
            con = sqlite3.connect('restaurantDB.sqlite')
            id_client, name_client = con.execute(f'SELECT id, name FROM tb_client WHERE phone = '
                                                 f'"{self.phone_le.text()}"').fetchone()
            name_staff = con.execute(f'SELECT name FROM tb_staff WHERE id = '
                                     f'{self.id_staff}').fetchone()[0]
            con.execute(f'INSERT INTO tb_order (id_staff, id_client) VALUES ({self.id_staff},'
                        f' {id_client})')
            id, time = con.execute('SELECT id, time FROM tb_order WHERE rowid=last_insert_rowid()').fetchone()
            row_count = self.orders_table.rowCount()
            self.orders_table.insertRow(row_count)
            self.orders_table.setItem(row_count, 0, QTableWidgetItem(str(id)))
            self.orders_table.setItem(row_count, 1, QTableWidgetItem(str(time)))
            self.orders_table.setItem(row_count, 2, QTableWidgetItem(str(name_client)))
            self.orders_table.setItem(row_count, 3, QTableWidgetItem(str(name_staff)))
            con.commit()
            self.close()
        except BaseException:
            self.mb_err = QMessageBox()
            self.mb_err.setIcon(QMessageBox.Warning)
            self.mb_err.setWindowTitle('Ошибка')
            self.mb_err.setText(f'Клиента с таким номером не существует')
            self.mb_err.setStandardButtons(QMessageBox.Ok)
            self.mb_err.show()
        finally:
            con.close()
