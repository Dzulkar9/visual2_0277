import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import mysql.connector

class MahasiswaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("datadiri.ui", self)  # Ganti dengan path ke file .ui kamu
        self.setWindowTitle("Aplikasi Data Mahasiswa")

        self.pushButton_3.clicked.connect(self.tambahData)
        self.pushButton_4.clicked.connect(self.editData)
        self.pushButton_5.clicked.connect(self.hapusData)
        self.pushButton.clicked.connect(self.clearForm)
        self.pushButton_2.clicked.connect(self.loadData)
        self.pushButton_6.clicked.connect(self.batal)
        self.tableWidget.cellClicked.connect(self.getData)

        self.selected_row = None

    def koneksi(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_latihan_0277"
        )

    def loadData(self):
        self.tableWidget.setRowCount(0)
        conn = self.koneksi()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mhs")
        result = cursor.fetchall()
        self.tableWidget.setRowCount(len(result))
        for row_num, row_data in enumerate(result):
            for col_num, data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        conn.close()

    def tambahData(self):
        nama = self.lineEdit.text()
        jurusan = self.lineEdit_2.text()

        if nama == "" or jurusan == "":
            QMessageBox.warning(self, "Peringatan", "Field tidak boleh kosong")
            return

        conn = self.koneksi()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mhs (nama, jurusan) VALUES (%s, %s)", (nama, jurusan))
        conn.commit()
        conn.close()

        self.loadData()
        self.clearForm()

    def batal(self):
        self.clearForm()
        self.loadData()

    def getData(self, row, col):
        self.selected_row = row
        self.lineEdit.setText(self.tableWidget.item(row, 0).text())
        self.lineEdit_2.setText(self.tableWidget.item(row, 1).text())

    def editData(self):
        if self.selected_row is None:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan diedit")
            return

        nama_baru = self.lineEdit.text()
        jurusan_baru = self.lineEdit_2.text()

        nama_lama = self.tableWidget.item(self.selected_row, 0).text()

        conn = self.koneksi()
        cursor = conn.cursor()
        cursor.execute("UPDATE mhs SET nama=%s, jurusan=%s WHERE nama=%s",
                       (nama_baru, jurusan_baru, nama_lama))
        conn.commit()
        conn.close()

        self.loadData()
        self.clearForm()

    def hapusData(self):
        if self.selected_row is None:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan dihapus")
            return

        nama = self.tableWidget.item(self.selected_row, 0).text()

        conn = self.koneksi()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mhs WHERE nama=%s", (nama,))
        conn.commit()
        conn.close()

        self.loadData()
        self.clearForm()

    def clearForm(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.selected_row = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MahasiswaApp()
    window.show()
    sys.exit(app.exec_())
