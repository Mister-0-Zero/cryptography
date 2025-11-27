def normalize_text(text: str = "Не все те повара, что с длинными ножами ходят.") -> str:
    norm_text = text.replace(" ", "").lower().replace(",", "зпт").replace(".", "тчк")
    return norm_text

def output_text(text: str, not_print = False) -> str:
    res = ""
    for ind, sim in enumerate(text):
        if ind % 5 == 0 and ind != 0:
            res += " "
        res += sim
    if not not_print: print(res)
    return res

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

