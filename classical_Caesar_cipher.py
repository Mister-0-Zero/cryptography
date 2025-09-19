def encoder(text):
    alf = "".join(sorted("йцукенгшщзхъфывапролджэячсмитьбю"))
    res = ""
    i = 0
    for sim in text:
        if sim in alf:
            idx = (alf.index(sim) - 3) % len(alf)
            res += alf[idx]
            i += 1
        if i % 5 == 0:
            res += " "
    
    return res

res = encoder("хиути рлицд легих диффл оярсж слзио гихеи олнлп флояр сжсхъ н")
print(res)