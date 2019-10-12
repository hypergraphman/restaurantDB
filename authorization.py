import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import *
from main import Main


class Authorization(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('authorization.ui', self)
        self.access_id = 0

        self.authorization_btn.clicked.connect(self.run)

    def run(self):
        con = sqlite3.connect('restaurantDB.sqlite')
        try:
            self.access_id, self.id_staff = con.execute(f'SELECT id_position, id FROM tb_staff WHERE phone = '
                                                        f'"{self.authorization_le.text()}"').fetchone()
        except BaseException:
            pass
        finally:
            con.close()

        if self.access_id != 0:
            self.hide()

            self.main_form = Main(self, self.access_id, self.id_staff)
            self.main_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Authorization()
    ex.show()
    sys.exit(app.exec())