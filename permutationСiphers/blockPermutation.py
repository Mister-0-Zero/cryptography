from baseFunctionForCryptography.baseFunction import *

print(f"{YELLOW}_______________ШИФР БЛОЧНОЙ ПЕРЕСТАНОВКИ__________________{RESET}")

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
    text_ = input("Введите текст для шифрования или Enter для моего текста: ")
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

L = len(text)

# ─────────────────────────────────────────────────────────
# Размер блока
# ─────────────────────────────────────────────────────────
while True:
    try:
        block_size = int(input("Введите размер блока (целое > 1): "))
    except ValueError:
        print(f"{RED}Нужно ввести целое число больше 1.{RESET}")
        continue
    if block_size <= 1:
        print(f"{RED}Размер блока должен быть больше 1.{RESET}")
        continue
    break

# ─────────────────────────────────────────────────────────
# Перестановка (ключ)
# ─────────────────────────────────────────────────────────
print(
    "Введите перестановку для блока длины",
    block_size,
    "в виде чисел от 1 до", block_size,
    "через пробел (например: 3 1 4 2).\n"
    "Enter = использовать обратный порядок (n, n-1, ..., 1)."
)

while True:
    line = input("Перестановка: ").strip()
    if line == "":
        perm = list(range(block_size - 1, -1, -1))  # 0..n-1, обратный порядок
        break

    parts = line.split()
    if len(parts) != block_size:
        print(f"{RED}Должно быть ровно {block_size} чисел.{RESET}")
        continue

    ok = True
    tmp = []
    for p in parts:
        if not p.isdigit():
            print(f"{RED}Все элементы должны быть числами от 1 до {block_size}.{RESET}")
            ok = False
            break
        v = int(p)
        if not (1 <= v <= block_size):
            print(f"{RED}Числа должны быть от 1 до {block_size}.{RESET}")
            ok = False
            break
        tmp.append(v - 1)  # перевод в 0-базу

    if not ok:
        continue

    if len(set(tmp)) != block_size:
        print(f"{RED}Числа в перестановке не должны повторяться.{RESET}")
        continue

    perm = tmp
    break

perm_str = " ".join(str(p + 1) for p in perm)

# ─────────────────────────────────────────────────────────
# Подготовка блоков
# ─────────────────────────────────────────────────────────
if is_encrypt:
    if L % block_size != 0:
        pad = block_size - (L % block_size)
        text_padded = text + "ф" * pad
    else:
        text_padded = text
    total_len = len(text_padded)
    blocks_count = total_len // block_size
else:
    if L % block_size != 0:
        print(f"{RED}Длина шифртекста не делится на размер блока. Проверьте ввод.{RESET}")
        exit(1)
    text_padded = text
    total_len = len(text_padded)
    blocks_count = total_len // block_size

blocks = [
    [text_padded[i * block_size + j] for j in range(block_size)]
    for i in range(blocks_count)
]

# ─────────────────────────────────────────────────────────
# ШИФРОВАНИЕ
# ─────────────────────────────────────────────────────────
if is_encrypt:
    cipher_blocks = []
    cipher_chars = []

    for b in blocks:
        new_block = [b[perm[i]] for i in range(block_size)]
        cipher_blocks.append(new_block)
        cipher_chars.extend(new_block)

    cipher_text = "".join(cipher_chars)

    print(f"{YELLOW}______________Отладочная информация (ШИФРОВАНИЕ)____________________{RESET}")
    print(f"{CYAN}Исходные блоки (после нормализации и дополнения 'ф' при необходимости):{RESET}")
    print_matrix(blocks)

    print(f"{CYAN}Блоки после перестановки:{RESET}")
    print_matrix(cipher_blocks)

    print(f"{GREEN}Размер блока: {block_size}{RESET}")
    print(f"{MAGENTA}Перестановка (позиции 1..n): {perm_str}{RESET}")

    print()
    print(f"{GREEN}Шифртекст (чтение блоков слева-направо, сверху-вниз):{RESET}")
    print(f"{WHITE_BRIGHT}{output_text(cipher_text, not_print=True)}{RESET}")

# ─────────────────────────────────────────────────────────
# РАСШИФРОВКА
# ─────────────────────────────────────────────────────────
else:
    cipher_blocks = blocks

    inv = [0] * block_size
    for i in range(block_size):
        inv[perm[i]] = i

    plain_blocks = []
    plain_chars = []

    for cb in cipher_blocks:
        orig_block = [None] * block_size
        for j in range(block_size):
            orig_block[j] = cb[inv[j]]
        plain_blocks.append(orig_block)
        plain_chars.extend(orig_block)

    plain_text = "".join(plain_chars)

    print(f"{YELLOW}______________Отладочная информация (РАСШИФРОВКА)__________________{RESET}")
    print(f"{CYAN}Блоки шифртекста:{RESET}")
    print_matrix(cipher_blocks)

    print(f"{CYAN}Блоки после обратной перестановки:{RESET}")
    print_matrix(plain_blocks)

    print(f"{GREEN}Размер блока: {block_size}{RESET}")
    print(f"{MAGENTA}Перестановка (позиции 1..n): {perm_str}{RESET}")

    print()
    print(f"{GREEN}Расшифрованный текст (последовательное чтение блоков):{RESET}")
    print(f"{WHITE_BRIGHT}{output_text(plain_text, not_print=True)}{RESET}")
