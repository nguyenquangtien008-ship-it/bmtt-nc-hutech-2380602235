class RailFenceCipher:
    def __init__(self):
        pass

    def validate_inputs(self, text, key_str):
        """Kiểm tra ràng buộc cho Rail Fence"""
        # 1. Kiểm tra văn bản trống
        if not text:
            return False, "Văn bản không được để trống!"
        
        # 2. Kiểm tra văn bản chỉ chứa chữ cái
        if any(not (c.isalpha() or c.isspace()) for c in text):
            return False, "Văn bản chỉ được chứa chữ cái!"
        
        # 3. Kiểm tra khóa có phải số không
        if not key_str.isdigit():
            return False, "Khóa (Key) phải là số nguyên dương!"
        
        num_rails = int(key_str)
        
        # 4. Kiểm tra điều kiện logic của Rail Fence
        if num_rails < 2:
            return False, "Khóa (Key) phải lớn hơn hoặc bằng 2!"
        if num_rails >= len(text):
            return False, f"Khóa (Key) phải nhỏ hơn độ dài văn bản ({len(text)} ký tự)!"
            
        return True, "OK"

    def rail_fence_encrypt(self, plain_text, num_rails):
        # Thuật toán cũ của bạn...
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1 
        for char in plain_text.replace(" ", ""): # Loại bỏ khoảng trắng để chuẩn hóa
            rails[rail_index].append(char)
            if rail_index == 0: direction = 1
            elif rail_index == num_rails - 1: direction = -1
            rail_index += direction
        return ''.join(''.join(rail) for rail in rails)

    def rail_fence_decrypt(self, cipher_text, num_rails):
        # Thuật toán cũ của bạn...
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0: direction = 1
            elif rail_index == num_rails - 1: direction = -1
            rail_index += direction

        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length

        plain_text = []
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            plain_text.append(rails[rail_index].pop(0))
            if rail_index == 0: direction = 1
            elif rail_index == num_rails - 1: direction = -1
            rail_index += direction
        return ''.join(plain_text)