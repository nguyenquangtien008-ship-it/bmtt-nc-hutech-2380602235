from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayfairCipher
from cipher.railfence import RailFenceCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)

#router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

# ================= CAESAR CIPHER =================
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    # --- RÀNG BUỘC THÊM ---
    if not (1 <= key <= 25): return "Lỗi: Khóa phải từ 1 đến 25"
    # -----------------------
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    # --- RÀNG BUỘC THÊM ---
    if not (1 <= key <= 25): return "Lỗi: Khóa phải từ 1 đến 25"
    # -----------------------
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ================= PLAYFAIR CIPHER =================
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

def get_matrix_html(key_string):
    Playfair = PlayfairCipher()
    matrix = Playfair.generate_matrix(key_string)
    html = "<table border='1' style='text-align:center; font-weight:bold; width:220px; margin:15px 0; border-collapse: collapse;'>"
    for row in matrix:
        html += "<tr style='height:40px;'>"
        for char in row:
            html += f"<td style='width:40px; border:1px solid #000; background-color:#f8f9fa;'>{char}</td>"
        html += "</tr>"
    html += "</table>"
    return html

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    # --- RÀNG BUỘC THÊM ---
    if not key.isalpha(): return "Lỗi: Khóa phải là chữ cái"
    # -----------------------
    Playfair = PlayfairCipher()
    encrypted_text = Playfair.encrypt_text(text, key)
    matrix_table = get_matrix_html(key)
    return f"<h4>KẾT QUẢ MÃ HÓA PLAYFAIR</h4>...{matrix_table} <b>Cipher Text:</b> {encrypted_text}"

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    # --- RÀNG BUỘC THÊM ---
    if not key.isalpha(): return "Lỗi: Khóa phải là chữ cái"
    # -----------------------
    Playfair = PlayfairCipher()
    decrypted_text = Playfair.decrypt_text(text, key)
    matrix_table = get_matrix_html(key)
    return f"<h4>KẾT QUẢ GIẢI MÃ PLAYFAIR</h4>...{matrix_table} <b>Plain Text:</b> {decrypted_text}"

# ================= RAIL FENCE CIPHER =================
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    # --- RÀNG BUỘC THÊM ---
    if key < 2: return "Lỗi: Khóa phải >= 2"
    # -----------------------
    RailFence = RailFenceCipher()
    encrypted_text = RailFence.rail_fence_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    # --- RÀNG BUỘC THÊM ---
    if key < 2: return "Lỗi: Khóa phải >= 2"
    # -----------------------
    RailFence = RailFenceCipher()
    decrypted_text = RailFence.rail_fence_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ================= VIGENERE CIPHER =================
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    # --- RÀNG BUỘC THÊM ---
    if not key.isalpha(): return "Lỗi: Khóa phải là chữ cái"
    # -----------------------
    Vigenere = VigenereCipher()
    encrypted_text = Vigenere.vigenere_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    # --- RÀNG BUỘC THÊM ---
    if not key.isalpha(): return "Lỗi: Khóa phải là chữ cái"
    # -----------------------
    Vigenere = VigenereCipher()
    decrypted_text = Vigenere.vigenere_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)