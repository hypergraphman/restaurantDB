import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import *
from addForm import AddForm
from editForm import EditForm


class Main(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('restaurant.ui', self)
        self.authorization_form = args[0]
        self.access_id = args[1]
        self.access_on()
        self.id_staff = args[2]

    def access_on(self):
        if self.access_id == 2:
            self.tabWidget.removeTab(3)
            self.tabWidget.removeTab(2)
            # По хорошему нужно было создать отдельный класс отображения всего этого хлама, НО
            # времени мало, поэтому во мне проснулся "индус" и я чего-то разочаровался в работе
            # с дизайнером qt, как-то он стимулирует "индусить"
            self.staff_show()  # в тот момент, когда я написал эту строчку я понял, что разделять
            # таблицу сотрудников и клиентов в моем случае было ошибкой =( НО редактировать БД
            # сейчас не позволительная роскошь и т.к. показ клиентов, сотрудников или блюд
            # практически ничем не отличаются, то я приступлю к работе с таблицой заказы, где
            # реализованна связь многие ко многим. Вспомнить и разобраться с этим гораздо интереснее
            self.clients_show()
        if self.access_id == 1:
            self.tabWidget.removeTab(0)
            # По хорошему нужно было создать отдельный класс отображения всего этого хлама, НО
            # времени мало, поэтому во мне проснулся "индус" и я чего-то разочаровался в работе
            # с дизайнером qt, как-то он стимулирует "индусить"
            self.clients_show()
            self.dish_show()
            self.orders_show()

    def orders_show(self):
        self.orders_table.setColumnWidth(0, 20)
        self.orders_table.setColumnWidth(1, 120)
        self.orders_table.setColumnWidth(2, 150)
        self.orders_table.setColumnWidth(3, 150)
        self.orders_table.setColumnWidth(4, 297)

        con = sqlite3.connect('restaurantDB.sqlite')

        for row_number, row in enumerate(con.execute('SELECT o.id, o.time, c.name, s.name FROM tb_order as o '
                                                     'JOIN tb_client as c ON c.id = o.id_client '
                                                     'JOIN tb_staff as s ON s.id = o.id_staff').fetchall()):
            self.orders_table.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.orders_table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

        con.close()

        self.add_order_btn.clicked.connect(self.add_order)
        self.del_order_btn.clicked.connect(self.del_order)
        self.order_id = ''
        self.orders_table.clicked.connect(self.click_orders_tbl)
        self.edit_order_btn.clicked.connect(self.edit_order)

    def staff_show(self):
        pass

    def dish_show(self):
        self.dish_table.insertRow(self.dish_table.rowCount())
        self.dish_table.setItem(self.dish_table.rowCount() - 1, 0, QTableWidgetItem('Введите название'))
        self.dish_table.setItem(self.dish_table.rowCount() - 1, 1, QTableWidgetItem('Введите цену'))
        self.dish_table.setColumnWidth(0, 400)

        con = sqlite3.connect('restaurantDB.sqlite')

        for row_number, row in enumerate(con.execute('SELECT name, cost FROM tb_dish').fetchall()):
            self.dish_table.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.dish_table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

        con.close()

        self.add_dish_btn.clicked.connect(self.add_dish)
        self.del_dish_btn.clicked.connect(self.del_dish)
        self.dish_name = ''
        self.dish_table.clicked.connect(self.click_dish_tbl)
        self.dish_table.cellChanged.connect(self.edit_dish)

    def clients_show(self):
        self.client_table.insertRow(self.client_table.rowCount())
        self.client_table.setItem(self.client_table.rowCount() - 1, 0, QTableWidgetItem('Введите имя'))
        self.client_table.setItem(self.client_table.rowCount() - 1, 1, QTableWidgetItem('Введите телефон'))
        self.client_table.setColumnWidth(0, 200)

        con = sqlite3.connect('restaurantDB.sqlite')

        for row_number, row in enumerate(con.execute('SELECT name, phone FROM tb_client').fetchall()):
            self.client_table.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.client_table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

        con.close()

        self.add_client_btn.clicked.connect(self.add_client)
        self.del_client_btn.clicked.connect(self.del_client)
        self.client_phone = ''
        self.client_table.clicked.connect(self.click_client_tbl)
        self.client_table.cellChanged.connect(self.edit_client)

    def add_dish(self):
        n_row = self.dish_table.rowCount() - 1
        n_col_1 = self.dish_table.columnCount() - 2
        n_col_2 = self.dish_table.columnCount() - 1
        name = self.dish_table.item(n_row, n_col_1).text()
        cost = self.dish_table.item(n_row, n_col_2).text()

        if name != 'Введите название' and cost != 'Введите цену':
            con = sqlite3.connect('restaurantDB.sqlite')
            try:
                con.execute(f'INSERT INTO tb_dish (name, cost) VALUES ("{name}",'
                            f' "{cost}")')

                con.commit()
                n_row += 1
                self.dish_table.insertRow(n_row)
                self.dish_table.setItem(n_row, n_col_1, QTableWidgetItem('Введите название'))
                self.dish_table.setItem(n_row, n_col_2, QTableWidgetItem('Введите цену'))

                self.mb_add = QMessageBox()
                self.mb_add.setIcon(QMessageBox.Information)
                self.mb_add.setWindowTitle('Блюдо добавлено')
                self.mb_add.setText(f'Блюдо {name} цена {cost}')
                self.mb_add.setStandardButtons(QMessageBox.Ok)
                self.mb_add.show()
            except BaseException:
                pass
            finally:
                con.close()

    def add_client(self):
        n_row = self.client_table.rowCount() - 1
        n_col_1 = self.client_table.columnCount() - 2
        n_col_2 = self.client_table.columnCount() - 1
        name = self.client_table.item(n_row, n_col_1).text()
        phone = self.client_table.item(n_row, n_col_2).text()

        if name != 'Введите имя' and phone != 'Введите телефон':
            con = sqlite3.connect('restaurantDB.sqlite')
            try:
                con.execute(f'INSERT INTO tb_client (name, phone) VALUES ("{name}",'
                            f' "{phone}")')

                con.commit()
                n_row += 1
                self.client_table.insertRow(n_row)
                self.client_table.setItem(n_row, n_col_1, QTableWidgetItem('Введите имя'))
                self.client_table.setItem(n_row, n_col_2, QTableWidgetItem('Введите телефон'))

                self.mb_add = QMessageBox()
                self.mb_add.setIcon(QMessageBox.Information)
                self.mb_add.setWindowTitle('Клиент добавлен')
                self.mb_add.setText(f'Клиент {name} {phone} добавлен')
                self.mb_add.setStandardButtons(QMessageBox.Ok)
                self.mb_add.show()
            except BaseException:
                pass
            finally:
                con.close()

    def add_order(self):
        self.add_order_form = AddForm(self.id_staff, self.orders_table)
        self.add_order_form.show()

    def edit_order(self):
        self.edit_order_form = EditForm(self.id_staff, self.orders_table)
        self.edit_order_form.show()

    def del_dish(self):
        if self.dish_table.currentRow() != self.dish_table.rowCount() - 1:
            con = sqlite3.connect('restaurantDB.sqlite')
            try:
                con.execute(f'DELETE FROM tb_dish '
                            f'WHERE name = "{self.dish_table.item(self.dish_table.currentRow(), 0).text()}"')

                con.commit()

                self.dish_table.removeRow(self.dish_table.currentRow())
            except BaseException:
                pass
            finally:
                con.close()

    def del_client(self):
        if self.client_table.currentRow() != self.client_table.rowCount() - 1:
            con = sqlite3.connect('restaurantDB.sqlite')
            try:
                con.execute(f'DELETE FROM tb_client '
                            f'WHERE phone = "{self.client_table.item(self.client_table.currentRow(), 1).text()}"')

                con.commit()

                self.client_table.removeRow(self.client_table.currentRow())
            except BaseException:
                pass
            finally:
                con.close()

    def del_order(self):
        con = sqlite3.connect('restaurantDB.sqlite')
        try:
            con.execute(f'DELETE FROM tb_order '
                        f'WHERE id = "{self.order_id}"')

            con.commit()

            self.orders_table.removeRow(self.orders_table.currentRow())
        except BaseException:
            pass
        finally:
            con.close()

    def click_client_tbl(self):
        self.client_phone = self.client_table.item(self.client_table.currentRow(), 1).text()

    def click_dish_tbl(self):
        self.dish_name = self.dish_table.item(self.dish_table.currentRow(), 0).text()

    def click_orders_tbl(self):
        self.order_id = self.orders_table.item(self.orders_table.currentRow(), 0).text()

    def edit_dish(self):
        if self.dish_table.currentRow() != self.dish_table.rowCount() - 1:
            if self.dish_table.currentColumn() == 0:
                with sqlite3.connect('restaurantDB.sqlite') as con:
                    sql = f'UPDATE tb_dish SET name = "{self.dish_table.currentItem().text()}" ' \
                          f'WHERE name = "{self.dish_name}"'
                    con.execute(sql)
                    con.commit()
            if self.dish_table.currentColumn() == 1:
                with sqlite3.connect('restaurantDB.sqlite') as con:
                    sql = f'UPDATE tb_dish SET cost = "{str(self.dish_table.currentItem().text())}" ' \
                          f'WHERE name = "{self.dish_name}"'
                    con.execute(sql)
                    con.commit()

    def edit_client(self):
        if self.client_table.currentRow() != self.client_table.rowCount() - 1:
            if self.client_table.currentColumn() == 0:
                with sqlite3.connect('restaurantDB.sqlite') as con:
                    sql = f'UPDATE tb_client SET name = "{self.client_table.currentItem().text()}" ' \
                          f'WHERE phone = "{self.client_phone}"'
                    con.execute(sql)
                    con.commit()
            if self.client_table.currentColumn() == 1:
                with sqlite3.connect('restaurantDB.sqlite') as con:
                    sql = f'UPDATE tb_client SET phone = "{self.client_table.currentItem().text()}" ' \
                          f'WHERE phone = "{self.client_phone}"'
                    con.execute(sql)
                    con.commit()

    # def closeEvent(self, *args, **kwargs):
    #     self.authorization_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    import authorization
    ex = Main(authorization.Authorization(), 1, 2)
    ex.show()
    sys.exit(app.exec_())
