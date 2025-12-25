# Vigenère Autokey (RU, без "ё"): encode/decode
from baseFunctionForCryptography.baseFunction import output_text as printer

RU_LOWER = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
RU_UPPER = RU_LOWER.upper()

def _norm_yo(s: str) -> str:
    return s.replace("ё", "е").replace("Ё", "Е")

def _only_ru_letters(s: str) -> str:
    s = _norm_yo(s)
    return "".join(ch for ch in s if ch in RU_LOWER or ch in RU_UPPER)

def _shifts_from_key(key: str):
    key = _only_ru_letters(key).lower()
    if not key:
        raise ValueError("Ключ должен содержать хотя бы одну русскую букву.")
    return [RU_LOWER.index(ch) for ch in key]

def vigenere_autokey_encrypt_ru(text: str, key: str) -> str:
    shifts = _shifts_from_key(key)[:]  # динамический поток сдвигов (ключ + plaintext)
    res, j = [], 0  # j — позиция среди БУКВ (небуквы пропускаем)

    for ch in text:
        ch2 = _norm_yo(ch)
        if ch2 in RU_LOWER or ch2 in RU_UPPER:
            alpha = RU_UPPER if ch2.isupper() else RU_LOWER
            n = len(alpha)
            p_idx = alpha.index(ch2)

            shift = shifts[j] if j < len(shifts) else 0  # страхуемся
            c_idx = (p_idx + shift) % n
            c = alpha[c_idx]
            res.append(c)

            # автоключ: добавляем ИСХОДНУЮ букву открытого текста (в нижнем регистре) в поток
            shifts.append(RU_LOWER.index(ch2.lower()))
            j += 1
        else:
            res.append(ch)
    return "".join(res)

def vigenere_autokey_decrypt_ru(text: str, key: str) -> str:
    # при декоде поток сдвигов пополняется уже ВОССТАНОВЛЕННЫМИ буквами plaintext
    shifts = _shifts_from_key(key)[:]
    res, j = [], 0

    for ch in text:
        ch2 = _norm_yo(ch)
        if ch2 in RU_LOWER or ch2 in RU_UPPER:
            alpha = RU_UPPER if ch2.isupper() else RU_LOWER
            n = len(alpha)
            c_idx = alpha.index(ch2)

            shift = shifts[j] if j < len(shifts) else 0
            p_idx = (c_idx - shift) % n
            p = alpha[p_idx]
            res.append(p)

            # добавляем восстановленную букву открытого текста в поток
            shifts.append(RU_LOWER.index(p.lower()))
            j += 1
        else:
            res.append(ch)
    return "".join(res)

# Пример
if __name__ == "__main__":
    phrase = "Не все те повара, что с длинными ножами ходят."
    key = "м"
    c = vigenere_autokey_encrypt_ru(phrase, key)
    d = vigenere_autokey_decrypt_ru(c, key)
    print("cipher :", printer(c))
    print("decoded:", printer(d))
