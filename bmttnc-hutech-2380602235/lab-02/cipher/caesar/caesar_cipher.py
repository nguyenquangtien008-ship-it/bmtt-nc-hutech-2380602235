# caesar_cipher.py
from cipher.caesar import ALPHABET # Giả sử file alphabet.py chứa chuỗi 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    # --- HÀM KIỂM TRA ĐIỀU KIỆN (Validation) ---
    def validate_inputs(self, text, key_str):
        if not text:
            return False, "Văn bản không được để trống!"
        
        # Kiểm tra xem có phải số nguyên không (không cho phép số âm)
        if not key_str.isdigit():
            return False, "Khóa (Key) phải là số nguyên dương!"
        
        key = int(key_str)
        
        # CHẶN SỐ ÂM VÀ GIỚI HẠN TỪ 1 ĐẾN 25
        if not (1 <= key <= 25):
            return False, "Khóa (Key) phải nằm trong khoảng từ 1 đến 25!"
            
        return True, "OK"

    # --- THUẬT TOÁN CHÍNH ---
    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        encrypted_text = []
        for letter in text:
            if letter.upper() in self.alphabet:
                is_upper = letter.isupper()
                idx = self.alphabet.index(letter.upper())
                new_idx = (idx + key) % alphabet_len
                char = self.alphabet[new_idx]
                encrypted_text.append(char if is_upper else char.lower())
            else:
                encrypted_text.append(letter)
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        # Giải mã là mã hóa với số bước là -key
        return self.encrypt_text(text, -key)