import numpy as np
from numpy.polynomial import polynomial


#функция преобразования в двоичный код
def text_bin(text,encoding="utf-8",errors = "surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding,errors),"big"))[2:]
    return bits.zfill(8*((len(bits)+7)//8))

#функция преобразования из двоичного кода
def textf(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


symbols = input("Символы для кодирования: ") #ввод
symbols = text_bin(symbols) #преобразование в двоичный код
print(symbols)
n_sum = int(input("Число сумматоров: "))


print("Дано регистров: 3")
sum_list = [] #список подключенных регистров к каждому сумматору
for i in range(n_sum): #подключение регистров к сумматору
    n_reg = int(input(f"Число подключаемых регистров для сумматора {i+1}: "))
    reg_list = [] #список регистров
    for j in range(n_reg):
        reg_list.append(int(input(f"Регистр {j+1}: ")))
        if reg_list[j] > 3: #ограничение регистров
            print("Ошибка: указан регистр > 3")
            exit()
    sum_list.append(reg_list)
print("")



coef_list = [] #список коэф. для составления полинома i(x)
for i in range(len(symbols)):
    coef_list.append(int(symbols[i]))
ix = np.poly1d(coef_list)  #функция из numpy, составляющая полином
print("i(x):")              #на основе списка
print(ix)
print("")


coef_list = [] #список с номерами регистров 1,0 (0,1,2)
for j in range(len(sum_list)):
    a = [0]*n_sum
    for i in range(len(sum_list[j])):
        a[sum_list[j][i]-1] = 1
    coef_list.append(a)
gx =[]
for i in range(n_sum): #составление полиномов g(x)
    gx.append(np.poly1d(coef_list[i]))
    print(f"g{i+1}(x):")
    print(np.poly1d(coef_list[i])) #ошибка, которая будет исправлена далее:
                                    #пропускает x^2 если были выбраны
                                    #регистры, например, 2 и 3 (коэф.: 1,2)
    print("")


cx = []
for i in range(len(gx)):
    cx.append(ix*gx[i]) #умножение i(x) * g(x)
f = []
for i in range(len(cx)): #убираем четные коэф., понадобится для создания
    for j in range(len(cx[i])):                                 #списка f
        if cx[i][j] % 2 == 0:
            cx[i][j] = 0
        else:
            cx[i][j] = 1
    print(f"C{i+1}(x):")
    print(cx[i])
    print("")
    f.append(np.asarray(cx[i].coef,list).tolist()) #создание списка f
                            #список из 0 и 1 (присутствие степени в полиноме)



#исправление ошибки
m = 0
for i in range(len(f)): #определяем максимальный m, чтобы добавить 0
    if m < len(f[i]):   #в место его отсутствия
        m = len(f[i])
for i in range(len(f)):
    f[i] = f[i][::-1] #reverse списка
    while len(f[i]) < m:
        f[i].append(0)



#создание частей закодированной последовательности
time = []
for i in range(len(f)): #забираем элемент из списка f
    if len(time) < len(f[i]):
        time = f[i]
f.remove(time)
if len(f) > 0:
    for i in range(len(f)): #и складываем его с остальными эл. списка f
        for j in range(len(f[i])):
            time[j] = str(time[j])+str(f[i][j]) #созд. частей закодир. послед.


#закодированная последовательность
code = ""
for i in range(len(time)):
    code = code + time[i]
print("Закодированные элементы:")
print(code)
print("")



#декодирование
print("Декодирование:")
razd = []
for i in range(0,len(code),n_sum): #разделение кода по степеням полиномов
    razd.append(code[i:i+n_sum])
print(razd)
print("")


i_x = []
for i in range(len(razd)): #берем первое число каждого элемента
    i_x.append(int(razd[i][0]))
i_x = i_x[::-1] #reverse
i_x = np.poly1d(i_x)
i_x = np.polydiv(i_x, gx[0]) #функция из numpy.polynomial делит полиномы
                                #(передаем делимое и делитель)
                                    #получаем i(x)
print(i_x[0])
print("")


i_coef = []
i_coef = np.asarray(i_x[0].coef,list).tolist() #список коэф. полинома i(x)
print(i_coef)
print("")
for i in range(len(i_coef)): #приведение полинома к нужному виду
    i_coef[i] = str(i_coef[i])
    i_coef[i] = i_coef[i].replace(".0","")
    i_coef[i] = i_coef[i].replace("-", "")
    if int(i_coef[i]) % 2 == 0:
        i_coef[i] = "0"
    else:
        i_coef[i] = "1"


code_again = ""
for i in range(len(i_coef)): #получившаяся закодированная последовательность
    code_again = code_again + str(i_coef[i])

print("Закодированные элементы:")
print(code_again)
print("")
print("Вы ввели символы:")
print(textf(code_again))
