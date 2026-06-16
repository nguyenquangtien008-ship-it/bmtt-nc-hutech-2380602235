def dao_nguoc_chuoi(chuoi):
    return chuoi[::-1]
input_string = input(print("Mời nhập chuỗi:"))
print("chuỗi đảo ngược là:", dao_nguoc_chuoi(input_string))