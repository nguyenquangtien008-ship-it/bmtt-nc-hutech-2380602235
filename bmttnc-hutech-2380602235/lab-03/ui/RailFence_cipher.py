import sys
from PyQt5 import QtWidgets
# Import giao diện Rail Fence từ file của bạn (sửa tên file nếu bạn đặt khác)
from RailFence import Ui_MainWindow 

class RailFenceStandaloneWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Thiết lập tiêu đề cửa sổ chuyên nghiệp
        self.setWindowTitle("Mô phỏng Mã hóa Rail Fence - Bảo mật thông tin")
        
        # Kết nối sự kiện nút bấm với hàm xử lý logic
        self.ui.pushButton.clicked.connect(self.encrypt_process)
        self.ui.pushButton_2.clicked.connect(self.decrypt_process)

    def rail_fence_encrypt(self, text, rails):
        """Thuật toán mã hóa Rail Fence (Xếp chuỗi theo hình zig-zag rồi đọc theo hàng)"""
        if rails <= 1 or rails >= len(text):
            return text
            
        # Tạo các hàng ray trống
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1 # 1: đi xuống, -1: đi lên
        
        for char in text:
            fence[rail].append(char)
            rail += direction
            
            # Đảo chiều khi chạm ray trên cùng hoặc dưới cùng
            if rail == rails - 1 or rail == 0:
                direction = -direction
                
        # Nối tất cả các hàng lại với nhau để tạo thành chuỗi mã hóa
        return "".join(["".join(r) for r in fence])

    def rail_fence_decrypt(self, cipher, rails):
        """Thuật toán giải mã Rail Fence (Tái cấu trúc lại ma trận zig-zag để đọc lại bản gốc)"""
        if rails <= 1 or rails >= len(cipher):
            return cipher
            
        # Bước 1: Đánh dấu các vị trí zig-zag bằng mảng chỉ số (index)
        template = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for i in range(len(cipher)):
            template[rail].append(i)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        # Gom các chỉ số theo thứ tự đọc từ trên xuống dưới, từ trái sang phải
        idx_map = []
        for r in template:
            idx_map.extend(r)
        
        # Bước 2: Tái cấu trúc chuỗi kết quả dựa trên bản đồ chỉ số
        result = [None] * len(cipher)
        for i, idx in enumerate(idx_map):
            result[idx] = cipher[i]
            
        return "".join(result)

    def encrypt_process(self):
        text = self.ui.plainTextEdit_3.toPlainText().strip()
        key_str = self.ui.plainTextEdit_2.toPlainText().strip()

        if not text: return

        # 1. Bẫy lỗi: Chỗ nhập chữ nhưng lại nhập số
        if any(char.isdigit() for char in text):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản (Text) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return

        # 2. Bẫy lỗi: Chỗ nhập số nhưng lại nhập chữ
        if not key_str.isdigit():
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) đường ray bắt buộc phải là SỐ!")
            return

        key = int(key_str)

        # 3. Ràng buộc: Số hàng ray phải nhỏ hơn độ dài văn bản và lớn hơn 1
        if key < 2 or key >= len(text):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", f"Khóa phải lớn hơn 1 và NHỎ HƠN độ dài văn bản (hiện tại là {len(text)} ký tự)!")
            return

        self.ui.plainTextEdit.setPlainText(self.rail_fence_encrypt(text, key))

    def decrypt_process(self):
        text = self.ui.plainTextEdit.toPlainText().strip()
        key_str = self.ui.plainTextEdit_2.toPlainText().strip()

        if not text: return

        if any(char.isdigit() for char in text):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản (Text) chỉ được chứa CHỮ CÁI, không được nhập số!")
            return

        if not key_str.isdigit():
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) đường ray bắt buộc phải là SỐ!")
            return

        key = int(key_str)

        if key < 2 or key >= len(text):
            QtWidgets.QMessageBox.warning(self, "Lỗi nhập liệu", f"Khóa phải lớn hơn 1 và NHỎ HƠN độ dài văn bản (hiện tại là {len(text)} ký tự)!")
            return

        self.ui.plainTextEdit_3.setPlainText(self.rail_fence_decrypt(text, key))


# =========================================================================
# KHỞI CHẠY ĐỘC LẬP
# =========================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion") # Đồng bộ giao diện phẳng
    
    window = RailFenceStandaloneWindow()
    window.show()
    sys.exit(app.exec_())