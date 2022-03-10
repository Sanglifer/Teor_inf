#операторы с приоритетом в виде словаря
OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}

def solution(expression):
    def parse(formula_string):
        number = '' #для "сборки" выражения
        for s in expression:
            if s in '1234567890.': # если символ - цифра, то собираем число
                number += s  
            elif number: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
                yield float(number) #возвращаем значение до...
                number = '' #...и собираем заного
            if s in OPERATORS or s in "()": # если символ - оператор или скобка, то выдаём как есть
                yield s #возвращаем оператор/скобку в виде символа
        if number:  # если в конце строки есть число, выдаём его
            yield float(number) #возвращаем число в формате float

    #алгоритм сортировочной станции
    #на входе объект из чисел и операторов в виде 3+4
    #на выходе числа и операторы в виде +34 (обратная польская запись)
    def sort_st(parsed_expression): 
        stack = []  # в качестве стэка используем список
        for token in parsed_expression:
            #если элемент - оператор, то отправляем дальше все операторы из стека, 
            #чей приоритет больше или равен пришедшему,
            #до открывающей скобки или опустошения стека.
            #здесь мы пользуемся тем, что все операторы имеют правую ассоциативность
            #т.е. вычисляются справа налево: 3+4 = 4+3
            if token in OPERATORS: 
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
                # а открывающую скобку выкидываем из стека.
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                # если элемент - открывающая скобка, просто положим её в стек
                stack.append(token)
            else:
                # если элемент - число, отправим его сразу на выход
                yield token
        while stack:
            yield stack.pop()

    #работа с записью выражения в виде +34
    def calc(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:  # если приходящий элемент - оператор,
                y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                stack.append(OPERATORS[token][1](x, y)) # вычисляем оператор, возвращаем в стек
            else:
                stack.append(token)
        return stack[0] # результат вычисления - единственный элемент в стеке


    return calc(sort_st(parse(expression)))

#расширенный алгоритм Евклида
#также определяет коэффициенты x и y
def Evklid(num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = Evklid(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)


expression = input('Введите выражение: ')
mod = int(input('Введите mod: '))
a = int(solution(expression))
print(f'{a} mod({mod}) = ?')
Ev = Evklid(a,mod)
if Ev[0] != 1:
    print(f'Нет решения. Числа {a} и {mod} не взаимнопростые (НОД = {Ev[0]})')
elif (Ev[0] == 1) and (mod != 0):
    print('-------------------------------')
    print(f'Числа {a} и {mod} взаимнопростые')
    print(f'x = {Ev[1]}, y = {Ev[2]}, НОД = {Ev[0]}')
    print('x*a + y*b = НОД')
    print(f'({Ev[1]}*{a}) + ({Ev[2]}*{mod}) = {Ev[0]}')
    print('-------------------------------')
    otvet = (Ev[1] % mod + mod) % mod
    print(f'Обратный элемент {a} в поле {mod}: {otvet}')
else:
    print(f'Нет решения. mod = {mod}')
