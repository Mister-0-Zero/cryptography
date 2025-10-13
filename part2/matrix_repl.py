chiper = "34,26,30,9,22,1,7,22,24,10,15,33,46,36,46,36,34,38,2,4,22,14,31,34,3,5,28,32,34,26,11,25,23,33,28,37,16,23,20,17,27,51,45,34,20,8,18,43,44,39,42,32,32"
alf = sorted("абвгдежзийклмнопрстуфхцчшщъыьэюя")

matrix = [[-0.5, 0.5, 0.5],
          [0.5, -0.5, 0.5],
          [0.5, 0.5, -0.5]]

chiper_mas = list(map(int, chiper.split(",")))

for i in range(len(chiper_mas) // 3):
    print(alf[round(matrix[0][0] * chiper_mas[i * 3] + 
          matrix[0][1] * chiper_mas[i * 3 + 1] + 
          matrix[0][2] * chiper_mas[i * 3 + 2]) - 1])
    print(alf[round(matrix[1][0] * chiper_mas[i * 3] + 
          matrix[1][1] * chiper_mas[i * 3 + 1] + 
          matrix[1][2] * chiper_mas[i * 3 + 2]) - 1])
    print(alf[round(matrix[2][0] * chiper_mas[i * 3] + 
          matrix[2][1] * chiper_mas[i * 3 + 1] + 
          matrix[2][2] * chiper_mas[i * 3 + 2]) - 1])
