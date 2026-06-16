from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# Khởi tạo các đối tượng thuật toán
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()

# Hàm hỗ trợ trả về lỗi chuẩn
def error_response(message):
    return jsonify({'error': message}), 400

# --- CAESAR ---
@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key_str = str(data.get('key', ''))
    is_valid, msg = caesar_cipher.validate_inputs(plain_text, key_str)
    if not is_valid: return error_response(msg)
    return jsonify({'encrypted_message': caesar_cipher.encrypt_text(plain_text, int(key_str))})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key_str = str(data.get('key', ''))
    is_valid, msg = caesar_cipher.validate_inputs(cipher_text, key_str)
    if not is_valid: return error_response(msg)
    return jsonify({'decrypted_message': caesar_cipher.decrypt_text(cipher_text, int(key_str))})

# --- VIGENERE ---
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key = data.get('key', '')
    is_valid, msg = vigenere_cipher.validate_inputs(plain_text, key)
    if not is_valid: return error_response(msg)
    return jsonify({'encrypted_text': vigenere_cipher.vigenere_encrypt(plain_text, key)})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', '')
    is_valid, msg = vigenere_cipher.validate_inputs(cipher_text, key)
    if not is_valid: return error_response(msg)
    return jsonify({'decrypted_text': vigenere_cipher.vigenere_decrypt(cipher_text, key)})

# --- RAIL FENCE ---
@app.route('/api/railfence/encrypt', methods=['POST'])
def rail_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key_str = str(data.get('key', ''))
    is_valid, msg = railfence_cipher.validate_inputs(plain_text, key_str)
    if not is_valid: return error_response(msg)
    return jsonify({'encrypted_text': railfence_cipher.rail_fence_encrypt(plain_text, int(key_str))})

@app.route('/api/railfence/decrypt', methods=['POST'])
def rail_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key_str = str(data.get('key', ''))
    is_valid, msg = railfence_cipher.validate_inputs(cipher_text, key_str)
    if not is_valid: return error_response(msg)
    return jsonify({'decrypted_text': railfence_cipher.rail_fence_decrypt(cipher_text, int(key_str))})

# --- PLAYFAIR ---
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key = data.get('key', '')
    # Kiểm tra cơ bản
    if not plain_text or not key: return error_response("Thiếu dữ liệu đầu vào!")
    matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'encrypted_text': playfair_cipher.playfair_encrypt(plain_text, matrix)})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', '')
    if not cipher_text or not key: return error_response("Thiếu dữ liệu đầu vào!")
    matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'decrypted_text': playfair_cipher.playfair_decrypt(cipher_text, matrix)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)