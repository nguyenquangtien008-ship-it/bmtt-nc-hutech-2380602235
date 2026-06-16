import sys
from PyQt5 import QtWidgets
# Import giao diện Vigenere từ file của bạn (sửa tên file nếu bạn đặt khác)
from Vigenere import Ui_MainWindow 

class VigenereStandaloneWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Thiết lập tiêu đề cửa sổ chuyên nghiệp và sửa chữ Label thô thành PlainText
        self.setWindowTitle("Mô phỏng Mã hóa Vigenere - Bảo mật thông tin")
        self.ui.label_3.setText("PlainText")
        
        # Kết nối sự kiện nút bấm với hàm xử lý logic
        self.ui.pushButton.clicked.connect(self.encrypt_process)
        self.ui.pushButton_2.clicked.connect(self.decrypt_process)

    def vigenere_cipher(self, text, key, decrypt=False):
        """Thuật toán mã hóa / giải mã Vigenere tuần hoàn khóa"""
        result = []
        key = key.upper()
        
        if not key.isalpha():
            raise ValueError("Mật khóa (Key) phải hoàn toàn là chữ cái từ A-Z!")
            
        key_index = 0
        for char in text:
            if char.isalpha():
                # Tính toán bước dịch chuyển dựa vào ký tự hiện tại của Key
                shift = ord(key[key_index % len(key)]) - 65
                if decrypt:
                    shift = -shift
                
                # Xử lý chữ hoa
                if char.isupper():
                    shifted = chr((ord(char) - 65 + shift) % 26 + 65)
                    result.append(shifted)
                # Xử lý chữ thường
                else:
                    shifted = chr((ord(char) - 97 + shift) % 26 + 97)
                    result.append(shifted)
                    
                key_index += 1  # Chỉ tăng vị trí khóa khi gặp ký tự chữ cái
            else:
                result.append(char) # Giữ nguyên khoảng trắng, số, ký tự đặc biệt
                
        return "".join(result)

    def encrypt_process(self):
        plaintext = self.ui.plainTextEdit_3.toPlainText().strip()
        key = self.ui.plainTextEdit_2.toPlainText().strip()
        
        if not plaintext: return
            
        if any(char.isdigit() for char in plaintext):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản (Plain text) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return
            
        if any(char.isdigit() for char in key):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return
            
        if not key:
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập mật khóa (Key)!")
            return
            
        ciphertext = self.vigenere_cipher(plaintext, key, decrypt=False)
        self.ui.plainTextEdit.setPlainText(ciphertext)

    def decrypt_process(self):
        ciphertext = self.ui.plainTextEdit.toPlainText().strip()
        key = self.ui.plainTextEdit_2.toPlainText().strip()
        
        if not ciphertext: return
            
        if any(char.isdigit() for char in ciphertext):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản (Cipher text) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return
            
        if any(char.isdigit() for char in key):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return
            
        if not key:
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập mật khóa (Key)!")
            return
            
        decrypted_text = self.vigenere_cipher(ciphertext, key, decrypt=True)
        self.ui.plainTextEdit_3.setPlainText(decrypted_text)


# =========================================================================
# KHỞI CHẠY ĐỘC LẬP TRỰC TIẾP TỪ FILE
# =========================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion") # Tạo phong cách giao diện hiện đại phẳng
    
    window = VigenereStandaloneWindow()
    window.show()
    sys.exit(app.exec_())