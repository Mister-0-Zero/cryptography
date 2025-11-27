def normalize_text(text: str = "Не все те повара, что с длинными ножами ходят.") -> str:
    norm_text = text.replace(" ", "").lower().replace(",", "зпт").replace(".", "тчк")
    return norm_text

def output_text(text: str) -> str:
    res = ""
    for ind, sim in enumerate(text):
        if ind % 5 == 0:
            res += " "
        res += sim
    print(res)
    return res

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"