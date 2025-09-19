# Bellaso (Vigenère-like) cipher for Russian without "ё".
# Encode/Decode with repeating key. Case preserved.

RU_LOWER = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
RU_UPPER = RU_LOWER.upper()

def _norm_yo(s: str) -> str:
    return s.replace("ё", "е").replace("Ё", "Е")

def _only_ru_letters(s: str) -> str:
    s = _norm_yo(s)
    return "".join(ch for ch in s if ch in RU_LOWER or ch in RU_UPPER)

def _key_shift(kch: str) -> int:
    return RU_LOWER.index(_norm_yo(kch).lower())

def bellaso_encrypt(text: str, key: str) -> str:
    k = _only_ru_letters(key)
    if not k:
        raise ValueError("Ключ должен содержать хотя бы одну русскую букву.")
    res, j = [], 0
    for ch in text:
        ch2 = _norm_yo(ch)
        if ch2 in RU_LOWER or ch2 in RU_UPPER:
            alpha = RU_UPPER if ch2.isupper() else RU_LOWER
            idx = alpha.index(ch2)
            shift = _key_shift(k[j % len(k)])
            res.append(alpha[(idx + shift) % len(alpha)])
            j += 1
        else:
            res.append(ch)
    return "".join(res)

def bellaso_decrypt(text: str, key: str) -> str:
    k = _only_ru_letters(key)
    if not k:
        raise ValueError("Ключ должен содержать хотя бы одну русскую букву.")
    res, j = [], 0
    for ch in text:
        ch2 = _norm_yo(ch)
        if ch2 in RU_LOWER or ch2 in RU_UPPER:
            alpha = RU_UPPER if ch2.isupper() else RU_LOWER
            idx = alpha.index(ch2)
            shift = _key_shift(k[j % len(k)])
            res.append(alpha[(idx - shift) % len(alpha)])
            j += 1
        else:
            res.append(ch)
    return "".join(res)

# Пример
if __name__ == "__main__":
    phrase = "не все те поваразпт что с длинными ножами ходяттчк"
    key = "гермес"
    c = bellaso_encrypt(phrase, key)
    d = bellaso_decrypt(c, key)
    print("cipher :", c)
    print("decoded:", d) 
