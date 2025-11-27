from baseFunctionForCryptography.baseFunction import *

text = normalize_text()

key = "машина"
count_col = len(key)
count_string = len(text) // count_col + 1 if len(text) % count_col != 0 else len(text) // count_col

matrix_sim = [[text[i * count_col + j] if (i * count_col + j) < len(text) else "-" for j in range(count_col)] for i in range(count_string)]

number_sim = [-1 for _ in range(count_col)]
num = 0
for sim in ALPHABET:
    if sim in key:
        for ind, sim_k in enumerate(key):
            if sim == sim_k:
                number_sim[ind] = num
                num += 1

chipper_text = ""

for number_col in range(count_col):
    j = number_sim.index(number_col)
    for i in range(count_string):
        chipper_text += matrix_sim[i][j]

print(f"{YELLOW}_______________ШИФР ВЕРТИКАЛЬНОЙ ПЕРЕСТАНОВКИ__________________{RESET}")
print(f"{YELLOW}______________Отладочная информация____________________{RESET}")

print(f"{CYAN}Матрица текста:{RESET}")
print_matrix(matrix_sim)

print(f"{GREEN}Заданный ключ: '{key}'{RESET}")

str_num = ''.join([str(num) for num in number_sim])
print(f"{MAGENTA}Номера букв в ключе: {str_num}{RESET}")

print()
print(f"{WHITE_BRIGHT}Зашифрованный текст: {output_text(chipper_text, not_print=True)}{RESET}")
