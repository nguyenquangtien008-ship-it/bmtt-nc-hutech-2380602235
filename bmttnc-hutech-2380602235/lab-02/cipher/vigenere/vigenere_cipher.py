class VigenereCipher:
    def __init__(self):
        pass

    def validate_inputs(self, text, key):
        """Kiểm tra ràng buộc cho Vigenere"""
        # 1. Kiểm tra văn bản trống
        if not text:
            return False, "Văn bản không được để trống!"
        
        # 2. Kiểm tra khóa trống
        if not key:
            return False, "Khóa (Key) không được để trống!"
            
        # 3. Kiểm tra khóa chỉ được chứa chữ cái (A-Z)
        if not key.isalpha():
            return False, "Khóa (Key) phải là chữ cái (không bao gồm số hoặc ký tự đặc biệt)!"
            
        return True, "OK"

    def vigenere_encrypt(self, plain_text, key):
        # Thuật toán cũ của bạn...
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        # Thuật toán cũ của bạn...
        decrypted_text = ""
        key_index = 0
        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text