from text_utils import *

#----------------------Функции шифрковки/расшифровки Виженера с самоключом---------------------
def encrypt_vigener_self_key(text:str, key:str) -> str:
    text = text.replace(" ", "")
    temp_text = ""
    temp_text += ALPHABET_U[(ALPHABET_U.find(text[0]) + ALPHABET_U.find(key))%len(ALPHABET_U)]
    for i, v in enumerate(text):
        if i == 0: continue 
        if i%5 == 0:
            temp_text += " "
        if ALPHABET_U.find(v) != -1:
            temp_text += ALPHABET_U[(ALPHABET_U.find(text[i-1]) + ALPHABET_U.find(v))%len(ALPHABET_U)]
        else: return "Not encrypted, wrong symbol in text"
    return temp_text

def decrypt_vigener_self_key(text:str, key:str) -> str:
    text = text.replace(" ", "")
    temp_text = ""
    first_letter = ALPHABET_U.find(text[0]) - ALPHABET_U.find(key)
    temp_text += ALPHABET_U[first_letter + len(ALPHABET_U) if first_letter < 0 else first_letter]
    for i, v in enumerate(text):
        if i == 0: continue 
        if ALPHABET_U.find(v) != -1:
            letter =  ALPHABET_U.find(v) - ALPHABET_U.find(temp_text[i-1])
            temp_text += ALPHABET_U[letter + len(ALPHABET_U) if letter < 0 else letter]
        else: return "Not decrypted, wrong symbol in text"
    temp2_text = ""
    for i,v in enumerate(temp_text):
        if i % 5 == 0 and i > 0: temp2_text += " "
        temp2_text += v
    return temp2_text
#-----------------------------------------------------------------------------------------------


#----------------------Функции шифрковки/расшифровки Виженера с шифртекстом---------------------
def encrypt_vigener_crypttext_key(text:str, key:str) -> str:
    text = text.replace(" ", "")
    temp_text = ""
    temp_text += ALPHABET_U[(ALPHABET_U.find(text[0]) + ALPHABET_U.find(key))%len(ALPHABET_U)]
    for i, v in enumerate(text):
        if i == 0: continue 
        if ALPHABET_U.find(v) != -1:
            temp_text += ALPHABET_U[(ALPHABET_U.find(temp_text[i-1]) + ALPHABET_U.find(v))%len(ALPHABET_U)]
        else: return "Not encrypted, wrong symbol in text"
    temp2_text = ""
    for i,v in enumerate(temp_text):
        if i % 5 == 0 and i > 0: temp2_text += " "
        temp2_text += v
    return temp2_text

def decrypt_vigener_crypttext_key(text:str, key:str) -> str:
    text = text.replace(" ", "")
    temp_text = ""
    first_letter = ALPHABET_U.find(text[0]) - ALPHABET_U.find(key)
    temp_text += ALPHABET_U[first_letter + len(ALPHABET_U) if first_letter < 0 else first_letter]
    for i, v in enumerate(text):
        if i == 0: continue 
        if ALPHABET_U.find(v) != -1:
            letter =  ALPHABET_U.find(v) - ALPHABET_U.find(text[i-1])
            temp_text += ALPHABET_U[letter + len(ALPHABET_U) if letter < 0 else letter]
        else: return "Not decrypted, wrong symbol in text"
    temp2_text = ""
    for i,v in enumerate(temp_text):
        if i % 5 == 0 and i > 0: temp2_text += " "
        temp2_text += v
    return temp2_text
#-----------------------------------------------------------------------------------------------


if __name__ == "__main__":
    text = "научись ходить прежде, чем будешь бегать."
    text_for_encryption = standartise(text)

    print(text_for_encryption)

    # print("aboba")
    # print(ALPHABET_U.index("А")+ALPHABET_U.index("А"))

    print(encrypt_vigener_self_key(text_for_encryption, "Б"))
    print(decrypt_vigener_self_key(encrypt_vigener_self_key(text_for_encryption, "Б"), "Б"))

    print()
    print(encrypt_vigener_crypttext_key(text_for_encryption, "Б"))
    print(decrypt_vigener_crypttext_key(encrypt_vigener_crypttext_key(text_for_encryption, "Б"), "Б"))
    print()
    print("Текст Паши:", decrypt_vigener_self_key("НАЩУЫ РЭНСВ ЛКВТО ЙЫСЛП ЦБЯНС ЫШЩЗЖ ШЭЭХЙ РЩКЭР БЯЮЯГ НИХЪЙ Б", "А"))
    print("Текст Пушкаша:", decrypt_vigener_crypttext_key("ЩЙЙЪВ ДЯЛУД ПЭЯЯЛ УВВУЕ КЪЗЗС ЮГТАМ МЭИРИ ДЦНЧ", "П"))

    #print(encrypt_vigener_self_key(text_for_encryption, "Т"))
