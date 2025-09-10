def get_dictonary_replace():
    alf = "".join(sorted("йцукенгшщзхъфывапролджэячсмитьбю"))
    res = {}
    flag = 0

    for num_str in range(6):
        for num_col in range(6):
            if num_str == 5 and num_col == 2:
                flag = 1
            if flag:
                break
            res[alf[num_str * 6 + num_col]] = f"{num_str + 1}{num_col + 1}"
        if flag:
            break
        
    return res


dict_replace = {'а': '11', 'б': '12', 'в': '13', 'г': '14', 'д': '15', 'е': '16', 'ж': '21', 'з': '22', 'и': '23', 'й': '24', 'к': '25', 'л': '26', 'м': '31', 'н': '32', 'о': '33', 'п': '34', 'р': '35', 'с': '36', 'т': '41', 'у': '42', 'ф': '43', 'х': '44', 'ц': '45', 'ч': '46', 'ш': '51', 'щ': '52', 'ъ': '53', 'ы': '54', 'ь': '55', 'э': '56', 'ю': '61', 'я': '62'}

my_str = "не все те поваразпт что с длинными ножами ходяттчк"

def encrypt(my_str, dict_replace):
    alf = "".join(sorted("йцукенгшщзхъфывапролджэячсмитьбю"))
    res = ""
    for sim in my_str:
        if sim in alf:
            res += f"{dict_replace[sim]} "
    
    return res

print(encrypt(my_str, dict_replace))