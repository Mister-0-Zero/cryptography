from baseFunctionForCryptography.baseFunction import *

# ─────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────

def _build_column_order(key: str) -> list[int]:
    """
    Строим порядок столбцов (number_sim) по алфавиту ALPHABET.
    """
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
        raise ValueError("Ошибка в ключе: не удалось построить перестановку столбцов.")

    return number_sim


def _matrix_to_lines(matrix: list[list[str]]) -> list[str]:
    return [" ".join(row) for row in matrix]


# ─────────────────────────────────────────────────────────
# Основные функции: шифрование / расшифровка
# ─────────────────────────────────────────────────────────

def encrypt_vertical(text: str, key: str) -> tuple[str, str]:
    """
    Шифрование вертикальной перестановкой.
    Возвращает (debug_text, cipher_text).
    """
    text_norm = normalize_encrypt(text=text)
    if len(text_norm) == 0:
        raise ValueError("Текст после нормализации пуст.")

    if not key:
        raise ValueError("Ключ не должен быть пустым.")

    key_norm = normalize_encrypt(text=key)
    if len(key_norm) == 0:
        raise ValueError("Ключ после нормализации пуст.")

    count_col = len(key_norm)
    L = len(text_norm)
    count_string = L // count_col + (1 if L % count_col != 0 else 0)

    matrix_sim = [
        [text_norm[i * count_col + j] if (i * count_col + j) < L else "-" for j in range(count_col)]
        for i in range(count_string)
    ]

    number_sim = _build_column_order(key_norm)

    chipper_text = ""
    for number_col in range(count_col):
        j = number_sim.index(number_col)
        for i in range(count_string):
            chipper_text += matrix_sim[i][j]

    chipper_text = chipper_text.replace("-", "")

    debug_lines: list[str] = []
    debug_lines.append("Матрица текста:")
    debug_lines.extend(_matrix_to_lines(matrix_sim))
    debug_lines.append("")
    debug_lines.append(f"Заданный ключ: '{key_norm}'")
    str_num = "".join(str(num) for num in number_sim)
    debug_lines.append(f"Номера букв в ключе: {str_num}")

    debug_text = "\n".join(debug_lines)
    return debug_text, chipper_text


def decrypt_vertical(cipher_text: str, key: str) -> tuple[str, str]:
    """
    Расшифровка вертикальной перестановки.
    Возвращает (debug_text, plain_text).
    """
    chipper_norm = normalize_decrypt(text=cipher_text)
    if len(chipper_norm) == 0:
        raise ValueError("Шифртекст после нормализации пуст.")

    if not key:
        raise ValueError("Ключ не должен быть пустым.")

    key_norm = normalize_decrypt(text=key)
    if len(key_norm) == 0:
        raise ValueError("Ключ после нормализации пуст.")

    count_col = len(key_norm)
    number_sim = _build_column_order(key_norm)

    L = len(chipper_norm)
    count_string = L // count_col + (1 if L % count_col != 0 else 0)

    cells = count_string * count_col
    pad_count = cells - L
    if pad_count > 0:
        last_row_filled = count_col - pad_count
    else:
        last_row_filled = count_col

    if last_row_filled <= 0 or last_row_filled > count_col:
        raise ValueError("Несоответствие длины шифртекста и ключа. Проверьте ввод.")

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
            raise ValueError("Несоответствие длины шифртекста и параметров матрицы.")
        matrix_sim[i][j] = chipper_norm[ind]
        ind += 1

    text_result = ""
    for i in range(count_string):
        for j in range(count_col):
            ch = matrix_sim[i][j]
            if ch != "-":
                text_result += ch

    debug_lines: list[str] = []
    debug_lines.append("Матрица шифртекста:")
    debug_lines.extend(_matrix_to_lines(matrix_sim))
    debug_lines.append("")
    debug_lines.append(f"Использованный ключ: '{key_norm}'")
    str_num = "".join(str(num) for num in number_sim)
    debug_lines.append(f"Номера букв в ключе: {str_num}")

    debug_text = "\n".join(debug_lines)
    return debug_text, text_result


# ─────────────────────────────────────────────────────────
# Простой CLI-режим для проверки
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"{YELLOW}_______________ШИФР ВЕРТИКАЛЬНОЙ ПЕРЕСТАНОВКИ (CLI)__________________{RESET}")

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

    if is_encrypt:
        while True:
            text_ = input("Введите свой текст для шифрования или Enter для моего текста: ")
            if text_ == "":
                text_raw = normalize_encrypt()
            else:
                text_raw = normalize_decrypt(text_)
            break

        while True:
            key_ = input("Введите ключ для шифрования или Enter для моего ключа: ")
            if key_ == "":
                key_raw = "машина"
            else:
                key_raw = normalize_encrypt(key_)
            if len(normalize_encrypt(text=key_raw)) == 0:
                print(f"{RED}Ключ после нормализации пуст. Введите другой ключ.{RESET}")
                continue
            break

        try:
            debug, result = encrypt_vertical(text_raw, key_raw)
            print(f"{YELLOW}______________Отладочная информация (ШИФРОВАНИЕ)____________________{RESET}")
            print(debug)
            print()
            print(f"{WHITE_BRIGHT}Зашифрованный текст: {output_encrypt(result, not_print=True)}{RESET}")
        except Exception as e:
            print(f"{RED}Ошибка: {e}{RESET}")

    else:
        while True:
            chipper_text_input = input("Введите зашифрованный текст: ")
            if len(normalize_decrypt(text=chipper_text_input)) == 0:
                print(f"{RED}Шифртекст после нормализации пуст. Введите другой текст.{RESET}")
                continue
            break

        while True:
            key_ = input("Введите ключ для расшифровки или Enter для моего ключа: ")
            if key_ == "":
                key_raw = "машина"
            else:
                key_raw = normalize_encrypt(key_)
            if len(normalize_encrypt(text=key_raw)) == 0:
                print(f"{RED}Ключ после нормализации пуст. Введите другой ключ.{RESET}")
                continue
            break

        try:
            debug, result = decrypt_vertical(chipper_text_input, key_raw)
            print(f"{YELLOW}______________Отладочная информация (РАСШИФРОВКА)__________________{RESET}")
            print(debug)
            print()
            print(f"{WHITE_BRIGHT}Расшифрованный текст: {output_decrypt(result, not_print=True)}{RESET}")
        except Exception as e:
            print(f"{RED}Ошибка: {e}{RESET}")