from baseFunctionForCryptography.baseFunction import *

# ─────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────

def _parse_permutation(block_size: int, perm_str: str) -> list[int]:
    perm_str = perm_str.strip()
    if block_size <= 1:
        raise ValueError("Размер блока должен быть больше 1.")

    if perm_str == "":
        return list(range(block_size - 1, -1, -1))

    parts = perm_str.split()
    if len(parts) != block_size:
        raise ValueError(f"Должно быть ровно {block_size} чисел в перестановке.")

    tmp: list[int] = []
    for p in parts:
        if not p.isdigit():
            raise ValueError("Все элементы перестановки должны быть числами.")
        v = int(p)
        if not (1 <= v <= block_size):
            raise ValueError(f"Числа перестановки должны быть от 1 до {block_size}.")
        tmp.append(v - 1)

    if len(set(tmp)) != block_size:
        raise ValueError("Числа в перестановке не должны повторяться.")

    return tmp


def _blocks_from_text(text: str, block_size: int) -> list[list[str]]:
    total_len = len(text)
    blocks_count = total_len // block_size
    return [
        [text[i * block_size + j] for j in range(block_size)]
        for i in range(blocks_count)
    ]


def _matrix_to_lines(blocks: list[list[str]]) -> list[str]:
    return [" ".join(b) for b in blocks]


# ─────────────────────────────────────────────────────────
# Основные функции: шифрование / расшифровка
# ─────────────────────────────────────────────────────────

def encrypt_block(text: str, block_size: int, perm_str: str = "") -> tuple[str, str]:
    text_norm = normalize_text(text=text)
    if len(text_norm) == 0:
        raise ValueError("Текст после нормализации пуст.")

    perm = _parse_permutation(block_size, perm_str)

    L = len(text_norm)
    if L % block_size != 0:
        pad = block_size - (L % block_size)
        text_padded = text_norm + "ф" * pad
    else:
        text_padded = text_norm

    blocks = _blocks_from_text(text_padded, block_size)

    cipher_blocks: list[list[str]] = []
    cipher_chars: list[str] = []

    for b in blocks:
        new_block = [b[perm[i]] for i in range(block_size)]
        cipher_blocks.append(new_block)
        cipher_chars.extend(new_block)

    cipher_text = "".join(cipher_chars)

    debug_lines: list[str] = []
    debug_lines.append("Исходные блоки (после нормализации и дополнения 'ф' при необходимости):")
    debug_lines.extend(_matrix_to_lines(blocks))
    debug_lines.append("")
    debug_lines.append("Блоки после перестановки:")
    debug_lines.extend(_matrix_to_lines(cipher_blocks))
    debug_lines.append("")
    debug_lines.append(f"Размер блока: {block_size}")
    debug_lines.append(f"Перестановка (позиции 1..n): {' '.join(str(p + 1) for p in perm)}")

    debug_text = "\n".join(debug_lines)
    return debug_text, cipher_text


def decrypt_block(cipher_text: str, block_size: int, perm_str: str = "") -> tuple[str, str]:
    text_norm = normalize_text(text=cipher_text)
    if len(text_norm) == 0:
        raise ValueError("Шифртекст после нормализации пуст.")

    if len(text_norm) % block_size != 0:
        raise ValueError("Длина шифртекста не делится на размер блока. Проверьте ввод.")

    perm = _parse_permutation(block_size, perm_str)

    blocks = _blocks_from_text(text_norm, block_size)

    inv = [0] * block_size
    for i in range(block_size):
        inv[perm[i]] = i

    plain_blocks: list[list[str]] = []
    plain_chars: list[str] = []

    for cb in blocks:
        orig_block = [None] * block_size
        for j in range(block_size):
            orig_block[j] = cb[inv[j]]
        plain_blocks.append(orig_block)
        plain_chars.extend(orig_block)

    plain_text = "".join(plain_chars)

    debug_lines: list[str] = []
    debug_lines.append("Блоки шифртекста:")
    debug_lines.extend(_matrix_to_lines(blocks))
    debug_lines.append("")
    debug_lines.append("Блоки после обратной перестановки:")
    debug_lines.extend(_matrix_to_lines(plain_blocks))
    debug_lines.append("")
    debug_lines.append(f"Размер блока: {block_size}")
    debug_lines.append(f"Перестановка (позиции 1..n): {' '.join(str(p + 1) for p in perm)}")

    debug_text = "\n".join(debug_lines)
    return debug_text, plain_text


# ─────────────────────────────────────────────────────────
# Простой CLI-режим для проверки (не мешает импорту в GUI)
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"{YELLOW}_______________ШИФР БЛОЧНОЙ ПЕРЕСТАНОВКИ (CLI)__________________{RESET}")

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
        text_ = input("Введите текст для шифрования или Enter для моего текста: ")
        if text_ == "":
            text_raw = normalize_text()
        else:
            text_raw = text_
    else:
        text_raw = input("Введите зашифрованный текст: ")

    try:
        block_size_cli = int(input("Введите размер блока (целое > 1): "))
    except ValueError:
        print(f"{RED}Неверный размер блока.{RESET}")
        exit(1)

    print(
        "Введите перестановку для блока длины",
        block_size_cli,
        "в виде чисел от 1 до", block_size_cli,
        "через пробел (например: 3 1 4 2).\n"
        "Enter = использовать обратный порядок (n, n-1, ..., 1)."
    )
    perm_line = input("Перестановка: ")

    try:
        if is_encrypt:
            debug, result = encrypt_block(text_raw, block_size_cli, perm_line)
            print(f"{YELLOW}______________Отладочная информация (ШИФРОВАНИЕ)____________________{RESET}")
            print(debug)
            print()
            print(f"{GREEN}Шифртекст:{RESET}")
            print(f"{WHITE_BRIGHT}{output_text(result, not_print=True)}{RESET}")
        else:
            debug, result = decrypt_block(text_raw, block_size_cli, perm_line)
            print(f"{YELLOW}______________Отладочная информация (РАСШИФРОВКА)__________________{RESET}")
            print(debug)
            print()
            print(f"{GREEN}Расшифрованный текст:{RESET}")
            print(f"{WHITE_BRIGHT}{output_text(result, not_print=True)}{RESET}")
    except Exception as e:
        print(f"{RED}Ошибка: {e}{RESET}")
