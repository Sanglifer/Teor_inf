from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 1) Вывод исходной картинки

filename = '10x10.jpg'  #исходная картинка
img = Image.open(filename)

img_arr = np.asarray(img) #массив пикселей
plt.axis('off')
plt.imshow(img_arr)
plt.savefig('1.jpg')    #исходная картинка будет хранится в 1.jpg
plt.show()

# 2) Зашумление картинки

img_arr.T.shape
img_bin = np.vectorize(np.binary_repr)(img_arr, width=8)    #значения пикселей в бинарный вид
rav = img_bin.copy().ravel()
for el in range(rav.shape[0]): #цикл зашумления картинки
    i = np.random.randint(0, 8)
    rav[el] = f'{rav[el][:i]}{int(rav[el][i]) ^ 1}{rav[el][i+1:]}'

img_err = rav.reshape(img_bin.shape) #зашумленные пиксели
pixels_err = np.array(list(map(lambda x: int(x, 2), list(img_err.ravel()))))
plt.axis('off')
plt.imshow(pixels_err.reshape(img_bin.shape))
plt.savefig('2.jpg')    #зашумленная картинка в 2.jpg
plt.show()
with open('img_bin.txt', 'w+') as outfile:
    outfile.write('# Array shape: {0}\n'.format(img_err.shape)) #количество пикселей картинки
    for slice_2d in img_bin: #срезы пикселей
        outfile.write('# New slice\n')
        np.savetxt(outfile, slice_2d, fmt='%s')


# 3) Декодирование и возвращение исходной картинки

#Gsys

left = np.identity(8).astype(int)   #левая часть матрицы - единичная часть
right = np.random.randint(0, 2, size=(8, 8))    #правая часть матрицы - задается рандомно
G_sys = np.hstack([left, right])    #стыкуем левую и правую часть

def xor(a: list):   #сумматор по модулю 2
    res = a[0]
    for el in a[1:]:
        res  = np.bitwise_xor(res, el)
    return res

d = np.array(range(2**8))
left_mat = (((d[:,None] & (1 << np.arange(8))[::-1])) > 0).astype(int)  #Hsys
rmat = np.zeros((2**8, 8))
for i, r in enumerate(left_mat[1:]):    #переворот
    a = right[np.nonzero(r)[0], :]
    rmat[i+1] = xor(a)  #xor Hsys
rmat = rmat.astype(int)
rc_mat = np.hstack([left_mat, rmat])    #стак левой и правой
res = np.hstack([left_mat, rc_mat, rc_mat.sum(axis=1).reshape(-1, 1)])
rmat = np.zeros((img_bin.ravel().shape[0], 16))
print(rmat.shape)
for i, r in enumerate(img_bin.ravel()): #переворот Gsys
    a = G_sys[np.nonzero(np.array(list(map(int, list(r)))))[0], :]
    if len(a) == 0:
        rmat[i] = np.zeros(16)
        continue
    rmat[i] = xor(a)
rmat = rmat.astype(int)
res = []
for el in rmat:
    res.append(np.array2string(el, separator='')[1:-1]) #массивы с ошибками попадут в bin16
bin_16 = np.array(res).reshape(img_bin.shape)   #формирование массивов
rav = bin_16.copy().ravel()
for el in range(rav.shape[0]):
    i = np.random.randint(0, 16)
    rav[el] = f'{rav[el][:i]}{int(rav[el][i]) ^ 1}{rav[el][i+1:]}'
bin_16_err = rav.reshape(img_bin.shape) #bin16_err - массив, в котором есть одна ошибка

with open('bin16.txt', 'w+') as outfile:
    outfile.write('# Array shape: {0}\n'.format(bin_16.shape))
    for slice_2d in bin_16:
        outfile.write('# New slice\n')
        np.savetxt(outfile, slice_2d, fmt='%s')

with open('bin16_err.txt', 'w+') as outfile:
    outfile.write('# Array shape: {0}\n'.format(bin_16.shape))
    for slice_2d in bin_16_err:
        outfile.write('# New slice\n')
        np.savetxt(outfile, slice_2d, fmt='%s')

H_t_sys = np.vstack((G_sys[:, 8:], G_sys[:, :8]))   #Gsys стак левого и правого ; формирование H_t_sys
vori = np.zeros((bin_16_err.ravel().shape[0], 8))
for i, r in enumerate(bin_16_err.ravel()):
    a = H_t_sys[np.nonzero(np.array(list(map(int, list(r)))))[0], :]
    if len(a) == 0:
        vori[i] = np.zeros(8)
        continue
    vori[i] = xor(a)

#S
#S = v * H_t_sys
#c' = v * H_t_sys + e
vori = vori.astype(int)
v = rc_mat[11]
v[2] = np.bitwise_not(v[2].astype(bool))
a = H_t_sys[np.nonzero(v)[0], :]
e = a[0]
for l in a[1:]:
#e
    e = np.bitwise_xor(e, l)
kpc = np.hstack([H_t_sys[::-1], np.rot90(np.identity(16).astype(int))]) #поворот на 90 градусов
eer = []
for v in vori:
    m = np.vectorize(np.bitwise_xor)(v, H_t_sys[::-1]).sum(axis=1).argmin()
    e = np.rot90(np.identity(16).astype(int))[m]
    eer.append(e)
eer = np.array(eer)
gumarner = []
for i, e in enumerate(bin_16_err.ravel()):  # v*h_t_sys+e ; c' - уже исправленный массив
    p = np.array(list(map(int, list(e))))
    k = np.bitwise_xor(p, eer[i])
    gumarner.append(k)
gumarner = np.array(gumarner)   #c', в которую записываем результат
res = []
for el in gumarner:
    res.append(np.array2string(el, separator='')[1:-1])
chisht = np.array(res).reshape(bin_16.shape)    #избавление от ошибки

from tqdm import tqdm

ier = []
for v in tqdm(gumarner):
    m = np.vectorize(np.bitwise_xor)(v, rc_mat).sum(axis=1).argmin()    #bin16 из скалярного значения получается числовое значение
    e = left_mat[m]
    ier.append(e)
#d
ier = np.array(ier) #в ier записывается матрица из bin16
res = []
for el in ier:
    res.append(int(''.join(list(map(str, el))), 2)) #деление по столбцам и по строкам
ver = np.array(res).reshape(bin_16.shape)
plt.axis('off')
plt.imshow(ver)
plt.savefig('3.jpg')
plt.show()