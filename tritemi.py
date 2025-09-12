# Trithemius cipher (progressive Caesar) — RU без "ё" + EN.
# E_i = (P_i + (start + i)) mod N;  D_i = (C_i - (start + i)) mod N

from typing import Tuple, Optional

EN_LOWER = "abcdefghijklmnopqrstuvwxyz"
EN_UPPER = EN_LOWER.upper()

# Русский алфавит БЕЗ "ё"
RU_LOWER = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
RU_UPPER = RU_LOWER.upper()

ALPHABETS: Tuple[Tuple[str, str], ...] = (
    (EN_LOWER, EN_UPPER),
    (RU_LOWER, RU_UPPER),
)

def _find_alphabet(ch: str) -> Optional[Tuple[str, str]]:
    for low, up in ALPHABETS:
        if ch in low or ch in up:
            return low, up
    return None

def _normalize_yo(ch: str) -> str:
    if ch == "ё":
        return "е"
    if ch == "Ё":
        return "Е"
    return ch

def trithemius(text: str, mode: str = "encode", start: int = 0) -> str:
    """
    mode: 'encode' | 'decode'
    start: начальное смещение (по умолчанию 0)
    Инкремент смещения идёт только по буквам.
    В RU 'ё/Ё' нормализуются в 'е/Е'.
    """
    if mode not in ("encode", "decode"):
        raise ValueError("mode must be 'encode' or 'decode'")

    res = []
    step = 0  # номер обработанной буквы

    for ch in text:
        ch2 = _normalize_yo(ch)
        ab = _find_alphabet(ch2)
        if not ab:
            res.append(ch)
            continue

        low, up = ab
        alpha = up if ch2.isupper() else low
        n = len(alpha)
        idx = alpha.index(ch2)

        shift = (start + step) % n
        if mode == "decode":
            shift = (-shift) % n

        res.append(alpha[(idx + shift) % n])
        step += 1

    return "".join(res)


# --- Короткая проверка ---
if __name__ == "__main__":
    plain = "не все те поваразпт что с длинными ножами ходяттчк"
    c = trithemius(plain, "encode", start=0)
    d = trithemius(c, "decode", start=0)
    print("cipher:", c)
    print("decoded:", d)
