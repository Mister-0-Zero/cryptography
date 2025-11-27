from baseFunctionForCryptography.baseFunction import *

print(f"{YELLOW}_______________ШИФР МАРШРУТНОЙ ПЕРЕСТАНОВКИ__________________{RESET}")

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
# Ввод текста
# ─────────────────────────────────────────────────────────
if is_encrypt:
    text_ = input("Введите свой текст для шифрования или Enter для моего текста: ")
    if text_ == "":
        text = normalize_text()
    else:
        text = normalize_text(text=text_)
else:
    text_ = input("Введите зашифрованный текст: ")
    text = normalize_text(text=text_)

if len(text) == 0:
    print(f"{RED}Текст после нормализации пуст. Завершение программы.{RESET}")
    exit(1)

# ─────────────────────────────────────────────────────────
# Параметры матрицы
# ─────────────────────────────────────────────────────────
while True:
    try:
        column_or_string = int(input("Введите 0 для выбора числа столбцов или 1 для выбора числа строк: "))
    except ValueError:
        print(f"{RED}Нужно ввести 0 или 1.{RESET}")
        continue
    if column_or_string in (0, 1):
        break
    print(f"{RED}Нужно ввести 0 или 1.{RESET}")

L = len(text)

if column_or_string == 0:
    while True:
        try:
            count_col = int(input("Введите число столбцов: "))
        except ValueError:
            print(f"{RED}Нужно ввести целое положительное число столбцов.{RESET}")
            continue
        if count_col <= 0:
            print(f"{RED}Число столбцов должно быть положительным.{RESET}")
            continue
        break
    count_string = L // count_col + 1 if L % count_col != 0 else L // count_col
else:
    while True:
        try:
            count_string = int(input("Введите число строк: "))
        except ValueError:
            print(f"{RED}Нужно ввести целое положительное число строк.{RESET}")
            continue
        if count_string <= 0:
            print(f"{RED}Число строк должно быть положительным.{RESET}")
            continue
        break
    count_col = L // count_string + 1 if L % count_string != 0 else L // count_string

cells = count_string * count_col
if cells < L:
    print(f"{RED}Размер матрицы меньше длины текста. Увеличьте число строк/столбцов.{RESET}")
    exit(1)

matrix = [
    ["ф" for _ in range(count_col)]
    for _ in range(count_string)
]

# ─────────────────────────────────────────────────────────
# Выбор маршрута
# ─────────────────────────────────────────────────────────
print("Выберете способ записи в таблицу, вам предлагается на выбор: ")
print("1) Змейка 1. Слева-направо, затем справа-налево")
print("2) Змейка 2. Справа-налево, затем слева-направо")
print("3) Вихрь по часовой стрелке")
print("4) Вихрь против часовой стрелки")
print("5) Снизу-вверх по столбцам")
print("6) Сверху-вниз по столбцам\n")

while True:
    try:
        vvod = int(input("Ваш ввод (1-6): "))
    except ValueError:
        print(f"{RED}Нужно ввести число от 1 до 6.{RESET}")
        continue
    if 1 <= vvod <= 6:
        break
    print(f"{RED}Нужно ввести число от 1 до 6.{RESET}")

rows = count_string
cols = count_col

# ─────────────────────────────────────────────────────────
# Формирование маршрута позиций
# ─────────────────────────────────────────────────────────
route_positions = []

if vvod == 1:
    # Змейка 1: слева-направо, затем справа-налево
    for i in range(rows):
        if i % 2 == 0:
            for j in range(cols):
                route_positions.append((i, j))
        else:
            for j in range(cols - 1, -1, -1):
                route_positions.append((i, j))

elif vvod == 2:
    # Змейка 2: справа-налево, затем слева-направо
    for i in range(rows):
        if i % 2 == 0:
            for j in range(cols - 1, -1, -1):
                route_positions.append((i, j))
        else:
            for j in range(cols):
                route_positions.append((i, j))

elif vvod == 3:
    # Вихрь по часовой
    top, bottom = 0, rows - 1
    left, right = 0, cols - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            route_positions.append((top, j))
        top += 1
        for i in range(top, bottom + 1):
            route_positions.append((i, right))
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                route_positions.append((bottom, j))
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                route_positions.append((i, left))
            left += 1

elif vvod == 4:
    # Вихрь против часовой
    top, bottom = 0, rows - 1
    left, right = 0, cols - 1
    while top <= bottom and left <= right:
        for i in range(top, bottom + 1):
            route_positions.append((i, left))
        left += 1
        for j in range(left, right + 1):
            route_positions.append((bottom, j))
        bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                route_positions.append((i, right))
            right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                route_positions.append((top, j))
            top += 1

elif vvod == 5:
    # Снизу-вверх по столбцам
    for j in range(cols):
        for i in range(rows - 1, -1, -1):
            route_positions.append((i, j))

elif vvod == 6:
    # Сверху-вниз по столбцам
    for j in range(cols):
        for i in range(rows):
            route_positions.append((i, j))

used_positions = route_positions[:L]
used_set = set(used_positions)

# ─────────────────────────────────────────────────────────
# ШИФРОВАНИЕ
# ─────────────────────────────────────────────────────────
if is_encrypt:
    for idx, (i, j) in enumerate(used_positions):
        matrix[i][j] = text[idx]

    print(f"{YELLOW}______________Отладочная информация (ШИФРОВАНИЕ)____________________{RESET}")
    print(f"{CYAN}Заполненная матрица (по маршруту):{RESET}")
    print_matrix(matrix)

    cipher_linear = ""
    for i in range(rows):
        for j in range(cols):
            if (i, j) in used_set:
                cipher_linear += matrix[i][j]

    print()
    print(f"{GREEN}Обычное чтение матрицы слева-направо, сверху-вниз (шифртекст):{RESET}")
    print(f"{WHITE_BRIGHT}{output_text(cipher_linear, not_print=True)}{RESET}")

# ─────────────────────────────────────────────────────────
# РАСШИФРОВКА
# ─────────────────────────────────────────────────────────
else:
    cipher_text = text
    if len(cipher_text) > cells:
        print(f"{RED}Длина шифртекста больше числа ячеек матрицы. Проверьте размеры.{RESET}")
        exit(1)

    used_positions = route_positions[:len(cipher_text)]
    used_set = set(used_positions)

    idx = 0
    for i in range(rows):
        for j in range(cols):
            if (i, j) in used_set:
                matrix[i][j] = cipher_text[idx]
                idx += 1

    plain_chars = []
    for (i, j) in used_positions:
        plain_chars.append(matrix[i][j])
    plain_text = "".join(plain_chars)

    print(f"{YELLOW}______________Отладочная информация (РАСШИФРОВКА)__________________{RESET}")
    print(f"{CYAN}Матрица, заполненная шифртекстом по строкам:{RESET}")
    print_matrix(matrix)

    print()
    print(f"{GREEN}Расшифрованный текст (чтение по маршруту):{RESET}")
    print(f"{WHITE_BRIGHT}{output_text(plain_text, not_print=True)}{RESET}")
