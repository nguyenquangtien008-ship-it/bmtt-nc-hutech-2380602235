import sys
import re
from PyQt5 import QtWidgets
# Import giao diện Playfair từ file của bạn (sửa tên file nếu bạn đặt khác)
from PlayFair import Ui_MainWindow 

class PlayfairStandaloneWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Đặt lại tiêu đề cửa sổ
        self.setWindowTitle("Mô phỏng Mã hóa Playfair - Bảo mật thông tin")
        
        # Kết nối sự kiện nút bấm với hàm xử lý logic
        self.ui.pushButton.clicked.connect(self.encrypt_process)
        self.ui.pushButton_2.clicked.connect(self.decrypt_process)

    def generate_matrix(self, key_str):
        """Khởi tạo ma trận Playfair 5x5 từ Khóa bí mật (gộp J thành I)"""
        key = key_str.upper().replace('J', 'I')
        key = re.sub(r'[^A-Z]', '', key)
        
        # Tạo danh sách ký tự không trùng lặp từ khóa và bảng chữ cái (bỏ J)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix_chars = []
        
        for char in (key + alphabet):
            if char not in matrix_chars:
                matrix_chars.append(char)
                
        # Cắt mảng phẳng thành ma trận 2 chiều 5x5
        return [matrix_chars[i:i+5] for i in range(0, 25, 5)]

    def find_position(self, matrix, char):
        """Tìm tọa độ (hàng, cột) của một ký tự trong ma trận 5x5"""
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return row, col
        return 0, 0

    def prepare_text(self, text):
        """Chuẩn hóa văn bản thô, xử lý cặp ký tự trùng nhau và độ dài lẻ"""
        text = text.upper().replace('J', 'I')
        text = re.sub(r'[^A-Z]', '', text) # Chỉ giữ lại ký tự chữ từ A-Z
        
        prepared = ""
        i = 0
        while i < len(text):
            n1 = text[i]
            # Nếu là ký tự cuối cùng của chuỗi lẻ, cặp với 'X'
            if (i + 1) >= len(text):
                prepared += n1 + 'X'
                i += 1
            else:
                n2 = text[i+1]
                if n1 == n2: # Nếu 2 ký tự trùng nhau đứng cạnh nhau, chèn 'X' vào giữa
                    prepared += n1 + 'X'
                    i += 1
                else:
                    prepared += n1 + n2
                    i += 2
        return prepared

    def playfair_cipher(self, text, key_str, mode='encrypt'):
        """Hàm xử lý thuật toán mã hóa / giải mã Playfair chính"""
        matrix = self.generate_matrix(key_str)
        
        if mode == 'encrypt':
            processed_text = self.prepare_text(text)
            shift = 1
        else: # decrypt
            processed_text = text.upper().replace('J', 'I')
            processed_text = re.sub(r'[^A-Z]', '', processed_text)
            shift = -1
            
        result = ""
        
        # Xử lý theo từng cặp 2 ký tự (Bigrams)
        for idx in range(0, len(processed_text), 2):
            r1, c1 = self.find_position(matrix, processed_text[idx])
            r2, c2 = self.find_position(matrix, processed_text[idx+1])
            
            if r1 == r2: # Trường hợp 1: Cùng hàng -> Dịch sang phải (hoặc trái)
                result += matrix[r1][(c1 + shift) % 5] + matrix[r2][(c2 + shift) % 5]
            elif c1 == c2: # Trường hợp 2: Cùng cột -> Dịch xuống dưới (hoặc lên trên)
                result += matrix[(r1 + shift) % 5][c1] + matrix[(r2 + shift) % 5][c2]
            else: # Trường hợp 3: Khác hàng và cột -> Đổi góc hình chữ nhật
                result += matrix[r1][c2] + matrix[r2][c1]
                
        return result

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
            
        ciphertext = self.playfair_cipher(plaintext, key, mode='encrypt')
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
            
        decrypted_text = self.playfair_cipher(ciphertext, key, mode='decrypt')
        self.ui.plainTextEdit_3.setPlainText(decrypted_text)


# =========================================================================
# KHỞI CHẠY TRỰC TIẾP KHÔNG QUA MAIN
# =========================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion") # Tạo giao diện phẳng hiện đại
    
    window = PlayfairStandaloneWindow()
    window.show()
    sys.exit(app.exec_())