def normalize_encrypt(text: str = "Не все те повара, что с длинными ножами ходят.") -> str:
    norm_text = text.replace(" ", "прб").lower().replace(",", "зпт").replace(".", "тчк")
    return norm_text

def normalize_decrypt(text: str) -> str:
    return text.replace(" ", "").lower()

def output_encrypt(text: str, not_print = True) -> str:
    res = ""
    for ind, sim in enumerate(text):
        if ind % 5 == 0 and ind != 0:
            res += " "
        res += sim
    if not not_print: print(res)
    return res

def output_decrypt(text: str, not_print = True) -> str:
    return text.replace("прб", " ").replace("зпт", ",").replace("тчк", ".")

def print_matrix(matrix):
    print()
    for string in matrix:
        print(string)
    print()


ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

RESET = "\033[0m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
WHITE_BRIGHT = "\033[97m"
RED = "\033[31m"

