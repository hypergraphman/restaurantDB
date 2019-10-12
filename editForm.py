import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import *


class EditForm(QDialog):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('edit_order.ui', self)
        self.id_staff = args[0]
        self.accept_btn.clicked.connect(self.edit_order)
        self.orders_table = args[1]

    def edit_order(self):
        try:
            con = sqlite3.connect('restaurantDB.sqlite')
            id_client, name_client = con.execute(f'SELECT id, name FROM tb_client WHERE phone = '
                                                 f'"{self.phone_le.text()}"').fetchone()
            # name_staff = con.execute(f'SELECT name FROM tb_staff WHERE id = '
            #                          f'{self.id_staff}').fetchone()[0]
            current_row = self.orders_table.currentRow()
            id = con.execute(f'SELECT id FROM tb_order '
                             f'WHERE id={self.orders_table.item(current_row, 0).text()}').fetchone()[0]
            time = con.execute('SELECT datetime("now")').fetchone()[0]
            print(time)
            sql = f'UPDATE tb_order SET id_client = "{id_client}", ' \
                  f'time = "{time}"  WHERE id = {id}'
            con.execute(sql)

            self.orders_table.setItem(current_row, 2, QTableWidgetItem(str(name_client)))
            self.orders_table.setItem(current_row, 1, QTableWidgetItem(str(time)))
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
