def encoder(text, shift):
    alf = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    res = ""
    i = 0
    for sim in text:
        if sim in alf:
            idx = (alf.index(sim) + shift) % len(alf)
            res += alf[idx]
            i += 1
        if i % 5 == 0:
            res += " "
    
    return res

res = encoder("не все те поваразпт что с длинными ножами ходяттчк", 13)
print(res)