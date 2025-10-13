alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
message = "Не все те повара, что с длинными ножами ходят."

# правило, то есть где XOR
rslos_reg1 = "10010" # 5 бит тут если че
rslos_reg1 = "11110" # -> x^5 + x^3 + 1
# Сам регистровый сдвиг, который меняется
start_value1 = "10000" # начальный ключ

rslos_reg2 = "1001" # типа добавочный регистр к 1 для 2 задания
start_value2 = "1000" # начальный ключ

new = "" # измененной сообщение (точки и прочее)

for i in range(len(message)):
    if message[i].lower() not in alpha:
        if message[i] == ",":
            new = new + "зпт"
        elif message[i] == ".":
            new = new + "тчк"
        elif message[i] == "-":
            new = new + "тре"
        else:
            new = new
    else:
        new = new + message[i].lower()

def shifr(l, rslos_reg1, start_value1):
    '''
    Сначала генерим весь ключ, потом накладываем
    l - какой длины ключ нужен в результате (длина сообщения в битах)

    Берем со старших разрядов - то есть слева направо ( по скринам с методы )

    return key - итоговая гамма вся
    '''

    key1 = ""
    for _ in range(l):
        key1 = key1 + start_value1[0]
        k = int(start_value1[0])
        for j in range(1, len(start_value1)):
            if rslos_reg1[j] == "1":
                k = k + int(start_value1[j])
        k = k % 2
        start_value1 = start_value1[1::] + str(k)
    return key1
    
def f(simb):
    '''
    'a' -> 00000
    ...
    'я' -> 11111
    '''
    res = 0
    for i in range(len(alpha)):
        if simb == alpha[i]:
            res = i

    b = "0" * (5 - len(str(bin(res)[2::]))) + str(bin(res)[2::])
    return b

def period(st):
    '''
    ищет период ключа
    '''
    for i in range(1, len(st)//2):
        check = 0
        for j in range(len(st)//i - 1):
            if st[j*i:(j+1)*i] != st[(j+1)*i:(j+2)*i]:
                check = 1
        if check == 0:
            return i
    return 0

def bin_sum(key1, bin_message):
    '''
    Накладываем гамму на инпут
    '''
    shifr1 = ""
    for i in range(len(bin_message)):
        shifr1 = shifr1 + str((int(key1[i]) + int(bin_message[i])) % 2)
    return shifr1

def tobukva(shifr1):
    '''
    00000 -> a
    ...
    11111 -> я
    '''
    alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    shifr_mess = ""
    for i in range(len(new)):
        a = shifr1[i*5:(i+1)*5]
        shifr_mess = shifr_mess + alpha[int(a, 2)]
    return shifr_mess

def tobin(new):
    bin_message = ""
    for i in range(len(new)):
        bin_message = bin_message + f(new[i])
    return bin_message

#шифруем 1 задание
bin_message = tobin(new) # перевели исходник в бинарное число
key1 = shifr(len(bin_message), rslos_reg1, start_value1) # сгенерили ключ нужной длины
shifr1 = bin_sum(key1, bin_message) # наложили гамму
result1 = tobukva(shifr1) # в буквы

print(result1)

#шифруем 2 задание
key2 = shifr(len(bin_message), rslos_reg1, start_value1)
key3 = shifr(len(bin_message), rslos_reg2, start_value2)
key_sum = bin_sum(key2, key3)
shifr2 = bin_sum(key_sum, bin_message)
result2 = tobukva(shifr2)

print(result2)

#дешифровка для 1 задания
bin_message1 = tobin(result1)
dekey = shifr(len(bin_message1), rslos_reg1, start_value1)
deshifr = bin_sum(dekey, bin_message1)
result3 = tobukva(deshifr)

print(result3)

#дешифровка для 2 задания
bin_message2 = tobin(result2)
dekey1 = shifr(len(bin_message2), rslos_reg1, start_value1)
dekey2 = shifr(len(bin_message2), rslos_reg2, start_value2)
key_res = bin_sum(dekey1, dekey2)
de2shifr = bin_sum(key_res, bin_message2)
result4 = tobukva(de2shifr)

print(result4)


key_test1 = shifr(100, rslos_reg1, start_value1)
key_test2 = shifr(1000, rslos_reg1, start_value1)
key_test3 = shifr(1000, rslos_reg2, start_value2)
key_test4 = bin_sum(key_test2, key_test3)

print(period(key_test1), "период для 1 задания")
print(period(key_test4), "период для 2 задания")
