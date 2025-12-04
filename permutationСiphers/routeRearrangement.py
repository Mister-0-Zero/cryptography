from baseFunctionForCryptography.baseFunction import *

# ─────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────

def _build_route_positions(rows: int, cols: int, mode: int) -> list[tuple[int, int]]:
    route_positions: list[tuple[int, int]] = []

    if mode == 1:
        for i in range(rows):
            if i % 2 == 0:
                for j in range(cols):
                    route_positions.append((i, j))
            else:
                for j in range(cols - 1, -1, -1):
                    route_positions.append((i, j))

    elif mode == 2:
        for i in range(rows):
            if i % 2 == 0:
                for j in range(cols - 1, -1, -1):
                    route_positions.append((i, j))
            else:
                for j in range(cols):
                    route_positions.append((i, j))

    elif mode == 3:
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

    elif mode == 4:
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

    elif mode == 5:
        for j in range(cols):
            for i in range(rows - 1, -1, -1):
                route_positions.append((i, j))

    elif mode == 6:
        for j in range(cols):
            for i in range(rows):
                route_positions.append((i, j))

    else:
        raise ValueError("Маршрут должен быть числом от 1 до 6.")

    return route_positions


def _matrix_to_lines(matrix: list[list[str]]) -> list[str]:
    return [" ".join(row) for row in matrix]


# ─────────────────────────────────────────────────────────
# Основные функции: шифрование / расшифровка
# ─────────────────────────────────────────────────────────

def encrypt_route(text: str, rows: int, cols: int, mode: int) -> tuple[str, str]:
    text_norm = normalize_encrypt(text=text)
    if len(text_norm) == 0:
        raise ValueError("Текст после нормализации пуст.")

    if rows <= 0 or cols <= 0:
        raise ValueError("Число строк и столбцов должно быть положительным.")

    L = len(text_norm)
    cells = rows * cols
    if cells < L:
        raise ValueError("Размер матрицы меньше длины текста. Увеличьте число строк/столбцов.")

    matrix = [["ф" for _ in range(cols)] for _ in range(rows)]
    route_positions = _build_route_positions(rows, cols, mode)
    used_positions = route_positions[:L]
    used_set = set(used_positions)

    for idx, (i, j) in enumerate(used_positions):
        matrix[i][j] = text_norm[idx]

    cipher_linear_chars: list[str] = []
    for i in range(rows):
        for j in range(cols):
            if (i, j) in used_set:
                cipher_linear_chars.append(matrix[i][j])
    cipher_text = "".join(cipher_linear_chars)

    debug_lines: list[str] = []
    debug_lines.append("Заполненная матрица (по маршруту):")
    debug_lines.extend(_matrix_to_lines(matrix))
    debug_lines.append("")
    debug_lines.append(f"Маршрут: режим {mode}, размер матрицы {rows}x{cols}")
    debug_text = "\n".join(debug_lines)

    return debug_text, cipher_text


def decrypt_route(cipher_text: str, rows: int, cols: int, mode: int) -> tuple[str, str]:
    text_norm = normalize_decrypt(text=cipher_text)
    if len(text_norm) == 0:
        raise ValueError("Шифртекст после нормализации пуст.")

    if rows <= 0 or cols <= 0:
        raise ValueError("Число строк и столбцов должно быть положительным.")

    L = len(text_norm)
    cells = rows * cols
    if L > cells:
        raise ValueError("Длина шифртекста больше числа ячеек матрицы. Проверьте размеры.")

    matrix = [["ф" for _ in range(cols)] for _ in range(rows)]
    route_positions = _build_route_positions(rows, cols, mode)
    used_positions = route_positions[:L]
    used_set = set(used_positions)

    idx = 0
    for i in range(rows):
        for j in range(cols):
            if (i, j) in used_set:
                matrix[i][j] = text_norm[idx]
                idx += 1

    plain_chars: list[str] = []
    for (i, j) in used_positions:
        plain_chars.append(matrix[i][j])
    plain_text = "".join(plain_chars)

    debug_lines: list[str] = []
    debug_lines.append("Матрица, заполненная шифртекстом по строкам:")
    debug_lines.extend(_matrix_to_lines(matrix))
    debug_lines.append("")
    debug_lines.append(f"Маршрут: режим {mode}, размер матрицы {rows}x{cols}")
    debug_text = "\n".join(debug_lines)

    return debug_text, plain_text


# ─────────────────────────────────────────────────────────
# Простой CLI-режим для проверки
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"{YELLOW}_______________ШИФР МАРШРУТНОЙ ПЕРЕСТАНОВКИ (CLI)__________________{RESET}")

    while True:
        mode_cli = input(
            "Выберите режим:\n"
            "1 - шифрование\n"
            "2 - расшифровка\n"
            "Ваш выбор (Enter = 1): "
        ).strip()
        if mode_cli in ("", "1", "2"):
            break
        print(f"{RED}Нужно ввести 1, 2 или Enter.{RESET}")

    is_encrypt = False if mode_cli == "2" else True

    if is_encrypt:
        text_ = input("Введите свой текст для шифрования или Enter для моего текста: ")
        if text_ == "":
            text_raw = normalize_encrypt()
        else:
            text_raw = normalize_encrypt(text_)
    else:
        text_raw = normalize_decrypt(input("Введите зашифрованный текст: "))

    while True:
        try:
            column_or_string = int(input("Введите 0 для выбора числа столбцов или 1 для выбора числа строк: "))
        except ValueError:
            print(f"{RED}Нужно ввести 0 или 1.{RESET}")
            continue
        if column_or_string in (0, 1):
            break
        print(f"{RED}Нужно ввести 0 или 1.{RESET}")

    if is_encrypt: L_cli = len(normalize_encrypt(text=text_raw))
    else: L_cli = len(normalize_decrypt(text=text_raw))

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
        count_string = L_cli // count_col + 1 if L_cli % count_col != 0 else L_cli // count_col
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
        count_col = L_cli // count_string + 1 if L_cli % count_string != 0 else L_cli // count_string

    cells_cli = count_string * count_col
    if cells_cli < L_cli:
        print(f"{RED}Размер матрицы меньше длины текста. Увеличьте число строк/столбцов.{RESET}")
        exit(1)

    print("Выберете способ записи в таблицу, вам предлагается на выбор: ")
    print("1) Змейка 1. Слева-направо, затем справа-налево")
    print("2) Змейка 2. Справа-налево, затем слева-направо")
    print("3) Вихрь по часовой стрелке")
    print("4) Вихрь против часовой стрелки")
    print("5) Снизу-вверх по столбцам")
    print("6) Сверху-вниз по столбцам\n")

    while True:
        try:
            vvod_cli = int(input("Ваш ввод (1-6): "))
        except ValueError:
            print(f"{RED}Нужно ввести число от 1 до 6.{RESET}")
            continue
        if 1 <= vvod_cli <= 6:
            break
        print(f"{RED}Нужно ввести число от 1 до 6.{RESET}")

    try:
        if is_encrypt:
            debug, result = encrypt_route(text_raw, count_string, count_col, vvod_cli)
            print(f"{YELLOW}______________Отладочная информация (ШИФРОВАНИЕ)____________________{RESET}")
            print(debug)
            print()
            print(f"{GREEN}Шифртекст:{RESET}")
            print(f"{WHITE_BRIGHT}{output_encrypt(result, not_print=True)}{RESET}")
        else:
            debug, result = decrypt_route(text_raw, count_string, count_col, vvod_cli)
            print(f"{YELLOW}______________Отладочная информация (РАСШИФРОВКА)__________________{RESET}")
            print(debug)
            print()
            print(f"{GREEN}Расшифрованный текст:{RESET}")
            print(f"{WHITE_BRIGHT}{output_decrypt(result, not_print=True)}{RESET}")
    except Exception as e:
        print(f"{RED}Ошибка: {e}{RESET}")
