import sys
from PyQt5 import QtWidgets
from caesar import Ui_MainWindow # Tên file UI bạn xuất ra từ Qt Designer

class CaesarWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Mô phỏng Mã hóa Caesar")
        self.ui.label_4.setText("CAESAR CIPHER")
        self.ui.label_3.setText("PlainText")
        
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)

    def cipher(self, text, step):
        res = []
        for c in text:
            if c.isupper(): res.append(chr((ord(c) - 65 + step) % 26 + 65))
            elif c.islower(): res.append(chr((ord(c) - 97 + step) % 26 + 97))
            else: res.append(c)
        return "".join(res)

    def encrypt(self):
        text = self.ui.plainTextEdit_3.toPlainText().strip()
        key_str = self.ui.plainTextEdit_2.toPlainText().strip()

        if not text: return

        # 1. Bẫy lỗi: Chỗ nhập chữ nhưng lại nhập số
        if any(char.isdigit() for char in text):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản (Text) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return

        # 2. Bẫy lỗi: Chỗ nhập số nhưng lại nhập chữ
        if not key_str.lstrip('-').isdigit(): # lstrip('-') cho phép nhập số âm
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) của Caesar bắt buộc phải là SỐ!")
            return

        key = int(key_str)

        # 3. Ràng buộc: Key từ 1 đến 25
        if not (1 <= key <= 25):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) của Caesar phải nằm trong khoảng từ 1 đến 25!")
            return

        # Vượt qua hết lỗi thì tiến hành mã hóa
        self.ui.plainTextEdit.setPlainText(self.cipher(text, key))

    def decrypt(self):
        text = self.ui.plainTextEdit.toPlainText().strip()
        key_str = self.ui.plainTextEdit_2.toPlainText().strip()

        if not text: return

        # 1. Bẫy lỗi: Chỗ nhập chữ nhưng lại nhập số
        if any(char.isdigit() for char in text):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản (Text) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return

        # 2. Bẫy lỗi: Chỗ nhập số nhưng lại nhập chữ
        if not key_str.lstrip('-').isdigit():
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) của Caesar bắt buộc phải là SỐ!")
            return

        key = int(key_str)

        # 3. Ràng buộc: Key từ 1 đến 25
        if not (1 <= key <= 25):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) của Caesar phải nằm trong khoảng từ 1 đến 25!")
            return

        # Vượt qua hết lỗi thì tiến hành giải mã
        self.ui.plainTextEdit_3.setPlainText(self.cipher(text, -key))


# ==========================================
# ĐOẠN NÀY GIÚP FILE CHẠY TRỰC TIẾP
# ==========================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")       # Giao diện hiện đại
    window = CaesarWindow()      # Gọi class của thuật toán này
    window.show()                # Hiển thị cửa sổ
    sys.exit(app.exec_())        # Giữ chương trình chạy