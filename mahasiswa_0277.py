import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector as mc

class MahasiswaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("mahasiswa.ui", self)  # Ganti sesuai nama file .ui kamu
        self.setWindowTitle("Form Mahasiswa")

        self.pushButton.clicked.connect(self.tambah)  # TAMBAH
        self.pushButton_2.clicked.connect(self.edit)  # UBAH
        self.pushButton_3.clicked.connect(self.hapus)  # HAPUS
        self.pushButton_4.clicked.connect(self.batal)  # BATAL
        self.tableWidget.cellClicked.connect(self.load_by_row)

        self.old_npm = "lineEdit.text()"
        self.load_data()

    def connect_db(self):
        return mc.connect(
            host="localhost",
            user="root",
            password="",
            database="mahasiswa_0277"
        )

    def tambah(self):
        try:
            db = self.connect_db()
            cursor = db.cursor()
            query = "INSERT INTO mhs (npm, nama, panggilan, telp, email, kelas, matkul) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (
                self.lineEdit.text(),
                self.lineEdit_2.text(),
                self.lineEdit_3.text(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                self.lineEdit_6.text(),
                self.lineEdit_7.text(),
            )
            cursor.execute(query, values)
            db.commit()
            self.statusBar().showMessage("Data berhasil ditambahkan")
            self.load_data()
            self.clear_form()
        except mc.Error as err:
            self.statusBar().showMessage(f"Masukan NPM yang benar")

    def edit(self):
        try:
            if not self.old_npm:
                self.statusBar().showMessage("Pilih data dari tabel dulu")
                return

            db = self.connect_db()
            cursor = db.cursor()
            query = """
                UPDATE mhs
                SET nama=%s, panggilan=%s, telp=%s, email=%s, kelas=%s, matkul=%s
                WHERE npm=%s
            """
            values = (
                self.lineEdit_2.text(),
                self.lineEdit_3.text(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                self.lineEdit_6.text(),
                self.lineEdit_7.text(),
                self.old_npm
            )
            cursor.execute(query, values)
            db.commit()
            self.statusBar().showMessage("Data berhasil diubah")
            self.load_data()
            self.clear_form()
        except mc.Error as err:
            self.statusBar().showMessage(f"Gagal edit: {err}")

    def hapus(self):
        try:
            db = self.connect_db()
            cursor = db.cursor()
            query = "DELETE FROM mhs WHERE npm=%s"
            cursor.execute(query, (self.lineEdit.text(),))
            db.commit()
            self.statusBar().showMessage("Data berhasil dihapus")
            self.load_data()
            self.clear_form()
        except mc.Error as err:
            self.statusBar().showMessage(f"Gagal hapus: {err}")

    def batal(self):
        self.clear_form()
        self.statusBar().showMessage("Form dibersihkan")

    def load_data(self):
        try:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM mhs")
            result = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            for row_num, row_data in enumerate(result):
                self.tableWidget.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        except mc.Error as err:
            self.statusBar().showMessage(f"Gagal load data: {err}")

    def load_by_row(self, row):
        self.lineEdit.setText(self.tableWidget.item(row, 0).text())
        self.lineEdit_2.setText(self.tableWidget.item(row, 1).text())
        self.lineEdit_3.setText(self.tableWidget.item(row, 2).text())
        self.lineEdit_4.setText(self.tableWidget.item(row, 3).text())
        self.lineEdit_5.setText(self.tableWidget.item(row, 4).text())
        self.lineEdit_6.setText(self.tableWidget.item(row, 5).text())
        self.lineEdit_7.setText(self.tableWidget.item(row, 6).text())
        self.old_npm = self.tableWidget.item(row, 0).text()

    def clear_form(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.old_npm = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MahasiswaApp()
    window.show()
    sys.exit(app.exec_())
