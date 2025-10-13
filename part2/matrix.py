A = [[1, 1, 1], 
     [0, 0, 1], 
     [1, 0, 1]]

text = "научись ходить прежде зпт чем будешь бегать тчк"

alf = sorted("абвгдежзийклмнопрстуфхцчшщъыьэюя")

text = text.replace(" ", "")

while len(text) % 3 != 0:
    text += 'ф'

print(text)

text_ = []

for sim in text:
    text_.append(alf.index(sim) + 1)

# print(text_)

for i in range(len(text) // 3):
    summ = []
    for mat in A:
        print(mat[0] * text_[i * 3] + mat[1] * text_[i * 3 + 1] + mat[2] * text_[i * 3 + 2], end =",")