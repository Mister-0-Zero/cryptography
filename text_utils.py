ALPHABET_U = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_L = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

#----------------Создание квадрата Тритемия из имеющегося алфавита----------------
ALPHABET_TRIT = []

for i in range(len(ALPHABET_U)):
    ALPHABET_TRIT.append(ALPHABET_U[i:] + ALPHABET_U[:i])
#---------------------------------------------------------------------------------

#---------------Функции для "стандартизации" строки под шифрование---------------
def convert_symbol(symbol:str) -> str:
    if symbol == ",": return "ЗПТ" 
    elif symbol == ".": return "ТЧК"
    elif symbol == " ": return ""
    elif ALPHABET_L.find(symbol) != -1: return ALPHABET_U[ALPHABET_L.find(symbol)]
    return symbol

def convert_string(text:str) -> str:
    temp_text = ""
    for i in text:
        temp_text += convert_symbol(i)
    return temp_text

def insert_spaces(text:str) -> str:
    temp_text = "" 
    for i, v in enumerate(text):
        temp_text += v
        if (i + 1) % 5 == 0 and i > 1:
            temp_text += " "
    return temp_text

def standartise(text:str) -> str:
    return insert_spaces(convert_string(text))
#--------------------------------------------------------------------------------


if __name__ == "__main__":
    
    ALPHABET_BELAZO = []
    for i in "АТБАШ":
        ALPHABET_BELAZO.append(ALPHABET_TRIT[ALPHABET_U.find(i)])

    for i in ALPHABET_BELAZO: print(*i)