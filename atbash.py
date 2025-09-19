alf = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

my_str = "не все те поваразпт что с длинными ножами ходяттчк"

i = 0
for sim in my_str:
    if sim != " ":
        index = alf.index(sim)
        ind_ = 31 - index
        print(alf[ind_], end="")
        i += 1
        if i % 5 == 0:
            print(" ", end="")