class PlayfairCipher:
    def __init__(self):
        pass

    # 1. Hàm tự động sinh ma trận 5x5 từ Khóa (Key)
    def generate_matrix(self, key):
        # Viết hoa, đổi J thành I, xóa khoảng trắng
        cleaned_key = key.upper().replace('J', 'I').replace(" ", "")
        
        matrix_chars = []
        # Điền các ký tự của Key vào trước (lọc trùng)
        for char in cleaned_key:
            if char.isalpha() and char not in matrix_chars:
                matrix_chars.append(char)
                
        # Điền các ký tự còn lại của bảng chữ cái (bỏ J)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in matrix_chars:
                matrix_chars.append(char)
                
        # Chuyển mảng phẳng 25 ký tự thành ma trận 2 chiều 5x5
        matrix_5x5 = [matrix_chars[i:i+5] for i in range(0, 25, 5)]
        return matrix_5x5

    # 2. Hàm tìm vị trí (dòng, cột) của một chữ cái trong ma trận
    def find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None, None

    # 3. Hàm chuẩn hóa văn bản đầu vào thành các cặp ký tự (Digraphs)
    def prepare_text(self, text):
        cleaned_text = text.upper().replace('J', 'I').replace(" ", "")
        prepared_chars = []
        
        i = 0
        while i < len(cleaned_text):
            char1 = cleaned_text[i]
            # Nếu là ký tự cuối cùng đơn lẻ, hoặc 2 ký tự liên tiếp trùng nhau thì chèn 'X'
            if i + 1 < len(cleaned_text):
                char2 = cleaned_text[i+1]
                if char1 == char2:
                    prepared_chars.append(char1)
                    prepared_chars.append('X')
                    i += 1
                else:
                    prepared_chars.append(char1)
                    prepared_chars.append(char2)
                    i += 2
            else:
                prepared_chars.append(char1)
                prepared_chars.append('X')
                i += 1
                
        return [prepared_chars[k:k+2] for k in range(0, len(prepared_chars), 2)]

    # 4. Hàm Mã Hóa (Encrypt)
    def encrypt_text(self, plain_text, key):
        matrix = self.generate_matrix(key)
        pairs = self.prepare_text(plain_text)
        cipher_chars = []
        
        for pair in pairs:
            r1, c1 = self.find_position(matrix, pair[0])
            r2, c2 = self.find_position(matrix, pair[1])
            
            if r1 == r2: # Cùng hàng: Dịch phải 1 cột (vòng lại đầu nếu chạm biên)
                cipher_chars.append(matrix[r1][(c1 + 1) % 5])
                cipher_chars.append(matrix[r2][(c2 + 1) % 5])
            elif c1 == c2: # Cùng cột: Dịch xuống 1 dòng (vòng lên đầu nếu chạm biên)
                cipher_chars.append(matrix[(r1 + 1) % 5][c1])
                cipher_chars.append(matrix[(r2 + 1) % 5][c2])
            else: # Khác hàng khác cột: Đổi góc hình chữ nhật
                cipher_chars.append(matrix[r1][c2])
                cipher_chars.append(matrix[r2][c1])
                
        return "".join(cipher_chars)

    # 5. Hàm Giải Mã (Decrypt)
    def decrypt_text(self, cipher_text, key):
        matrix = self.generate_matrix(key)
        cleaned_cipher = cipher_text.upper().replace(" ", "")
        pairs = [list(cleaned_cipher[i:i+2]) for i in range(0, len(cleaned_cipher), 2)]
        plain_chars = []
        
        for pair in pairs:
            if len(pair) < 2: continue
            r1, c1 = self.find_position(matrix, pair[0])
            r2, c2 = self.find_position(matrix, pair[1])
            
            if r1 == r2: # Cùng hàng: Dịch trái 1 cột
                plain_chars.append(matrix[r1][(c1 - 1) % 5])
                plain_chars.append(matrix[r2][(c2 - 1) % 5])
            elif c1 == c2: # Cùng cột: Dịch lên 1 dòng
                plain_chars.append(matrix[(r1 - 1) % 5][c1])
                plain_chars.append(matrix[(r2 - 1) % 5][c2])
            else: # Khác hàng khác cột: Đổi góc hình chữ nhật
                plain_chars.append(matrix[r1][c2])
                plain_chars.append(matrix[r2][c1])
                
        return "".join(plain_chars)