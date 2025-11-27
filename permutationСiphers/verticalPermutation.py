from baseFunctionForCryptography.baseFunction import *

print(f"{YELLOW}_______________ШИФР ВЕРТИКАЛЬНОЙ ПЕРЕСТАНОВКИ__________________{RESET}")

# ─────────────────────────────────────────────────────────
# Выбор режима
# ─────────────────────────────────────────────────────────
while True:
    mode = input(
        "Выберите режим:\n"
        "1 - шифрование\n"
        "2 - расшифровка\n"
        "Ваш выбор (Enter = 1): "
    ).strip()
    if mode in ("", "1", "2"):
        break
    print(f"{RED}Нужно ввести 1, 2 или Enter.{RESET}")

is_encrypt = False if mode == "2" else True

# ─────────────────────────────────────────────────────────
# Ввод текста и ключа
# ─────────────────────────────────────────────────────────
if is_encrypt:
    while True:
        text_ = input("Введите свой текст для шифрования или Enter для моего текста: ")
        if text_ == "":
            text = normalize_text()
        else:
            text = normalize_text(text=text_)
        if len(text) == 0:
            print(f"{RED}Текст после нормализации пуст. Введите другой текст.{RESET}")
            continue
        break

    while True:
        key_ = input("Введите ключ для шифрования или Enter для моего ключа: ")
        if key_ == "":
            key = "машина"
        else:
            key = normalize_text(text=key_)
        if len(key) == 0:
            print(f"{RED}Ключ после нормализации пуст. Введите другой ключ.{RESET}")
            continue
        break

    chipper_text_input = None
else:
    while True:
        chipper_text_input = input("Введите зашифрованный текст: ")
        chipper_text_input = normalize_text(text=chipper_text_input)
        if len(chipper_text_input) == 0:
            print(f"{RED}Шифртекст после нормализации пуст. Введите другой текст.{RESET}")
            continue
        break

    while True:
        key_ = input("Введите ключ для расшифровки или Enter для моего ключа: ")
        if key_ == "":
            key = "машина"
        else:
            key = normalize_text(text=key_)
        if len(key) == 0:
            print(f"{RED}Ключ после нормализации пуст. Введите другой ключ.{RESET}")
            continue
        break

# ─────────────────────────────────────────────────────────
# Общие параметры: ключ и номера столбцов
# ─────────────────────────────────────────────────────────
count_col = len(key)

number_sim = [-1 for _ in range(count_col)]
num = 0
for sim in ALPHABET:
    if sim in key:
        for ind, sim_k in enumerate(key):
            if sim == sim_k and number_sim[ind] == -1:
                number_sim[ind] = num
                num += 1

if -1 in number_sim:
    print(f"{RED}Ошибка в ключе: не удалось построить перестановку столбцов.{RESET}")
    exit(1)

# ─────────────────────────────────────────────────────────
# ШИФРОВАНИЕ
# ─────────────────────────────────────────────────────────
if is_encrypt:
    count_string = len(text) // count_col + 1 if len(text) % count_col != 0 else len(text) // count_col

    matrix_sim = [
        [text[i * count_col + j] if (i * count_col + j) < len(text) else "-" for j in range(count_col)]
        for i in range(count_string)
    ]

    chipper_text = ""

    for number_col in range(count_col):
        j = number_sim.index(number_col)
        for i in range(count_string):
            chipper_text += matrix_sim[i][j]

    chipper_text = chipper_text.replace("-", "")

    print(f"{YELLOW}______________Отладочная информация (ШИФРОВАНИЕ)____________________{RESET}")

    print(f"{CYAN}Матрица текста:{RESET}")
    print_matrix(matrix_sim)

    print(f"{GREEN}Заданный ключ: '{key}'{RESET}")

    str_num = ''.join([str(num) for num in number_sim])
    print(f"{MAGENTA}Номера букв в ключе: {str_num}{RESET}")

    print()
    print(f"{WHITE_BRIGHT}Зашифрованный текст: {output_text(chipper_text, not_print=True)}{RESET}")

# ─────────────────────────────────────────────────────────
# РАСШИФРОВКА
# ─────────────────────────────────────────────────────────
else:
    chipper_text = chipper_text_input
    L = len(chipper_text)

    count_string = L // count_col + 1 if L % count_col != 0 else L // count_col

    cells = count_string * count_col
    pad_count = cells - L

    if pad_count > 0:
        last_row_filled = count_col - pad_count
    else:
        last_row_filled = count_col

    if last_row_filled <= 0 or last_row_filled > count_col:
        print(f"{RED}Несоответствие длины шифртекста и ключа. Проверьте ввод.{RESET}")
        exit(1)

    matrix_sim = [["-" for _ in range(count_col)] for _ in range(count_string)]

    positions = []
    for number_col in range(count_col):
        j = number_sim.index(number_col)
        for i in range(count_string):
            positions.append((i, j))

    pad_positions = set()
    if pad_count > 0:
        for col in range(last_row_filled, count_col):
            pad_positions.add((count_string - 1, col))

    ind = 0
    for (i, j) in positions:
        if (i, j) in pad_positions:
            continue
        if ind >= L:
            print(f"{RED}Несоответствие длины шифртекста и параметров матрицы.{RESET}")
            exit(1)
        matrix_sim[i][j] = chipper_text[ind]
        ind += 1

    text_result = ""
    for i in range(count_string):
        for j in range(count_col):
            ch = matrix_sim[i][j]
            if ch != "-":
                text_result += ch

    print(f"{YELLOW}______________Отладочная информация (РАСШИФРОВКА)__________________{RESET}")

    print(f"{CYAN}Матрица шифртекста:{RESET}")
    print_matrix(matrix_sim)

    print(f"{GREEN}Использованный ключ: '{key}'{RESET}")

    str_num = ''.join([str(num) for num in number_sim])
    print(f"{MAGENTA}Номера букв в ключе: {str_num}{RESET}")

    print()
    print(f"{WHITE_BRIGHT}Расшифрованный текст: {text_result}{RESET}")
