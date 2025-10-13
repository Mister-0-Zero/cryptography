def printer(text):
    i = 0
    res = ""
    for sim in text:
        if i % 5 == 0:
            res += " "
        if sim in "абвгдежзийклмнопрстуфхцчшщъыьэюя":
            res += sim
            i += 1
    return res