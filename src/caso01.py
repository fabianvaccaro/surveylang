import numpy as np
import re

"""
Para segmentos
S <- ID del segmento
X <- Valor a buscar

IN(X, S)
True si X en S

COUNT(X, S)
True si len(S) == X


SLT(X, S)
True si algún elemento de S es menor estricto que X

SLTE(X, S)
True si algún elemento de S es menor o igual que X

SGT(X, S)
True si algún elemento de S es mayor estricto que X

SGTE(X, S)
True si algún elemento de S es mayor o igual que X


Para Items
I <- ID del item
X <- Valor a buscar

EQ(X, I)
True si X == I

LT(X, I)
True si X < I

LTE(X, I)
True si X <= I

GT(X, I)
True si X > I

GTE(X, I)
True si X >= I

Operadores lógicos
ANY(_, _, _, ...)
True si alguno de los argumentos es True


ALL(_, _, _, ...)
True si todos los argumentos son True


NOT(_)
Negación lógica

"""
segment_arr = [[1, 2, 3], [9], [1, 9], [99], [6, 8]]


# Returns the position of the commas that has the same number of ( and ) before its appearance
def get_position_of_comma(x: str):
    res = []
    count = 0
    for i in range(len(x)):
        if x[i] == '(':
            count += 1
        elif x[i] == ')':
            count -= 1
        elif x[i] == ',':
            if count == 0:
                res.append(i)
    return res+[len(x)]


def extract_parameters(x: str):
    res = re.findall(r'\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)', x)
    if len(res) != 1:
        raise ValueError('La sentencia no está correctamente escrita')
    res = res[0][1:-1]

    # split string by indices
    indices = get_position_of_comma(res)
    parameters = []

    parameters.append(res[0:indices[0]])
    for i in range(len(indices)-1):
        parameters.append(res[indices[i]+1:indices[i+1]])

    return parameters


def _in(x, s):
    return int(x) in segment_arr[int(s)]


def _count(x, s):
    return len(segment_arr[int(s)]) == int(x)


def _slt(x, s):
    return any([i < int(x) for i in segment_arr[int(s)]])


def _slte(x, s):
    return any([i <= int(x) for i in segment_arr[int(s)]])


def _sgt(x, s):
    return any([i > int(x) for i in segment_arr[int(s)]])


def _sgte(x, s):
    return any([i >= int(x) for i in segment_arr[int(s)]])


def _all(x):
    return all([eval(i) for i in x])


def _any(x):
    return any([eval(i) for i in x])


def eval(x: str):
    functions = {'ALL': (_all, -1), 'ANY': (_any, -1), 'IN': (_in, 2), 'COUNT': (_count, 2), 'SLT': (_slt, 2),
                 'SLTE': (_slte, 2), 'SGT': (_sgt, 2), 'SGTE': (_sgte, 2)}
    operation = x.split('(')[0].strip()
    parameters = extract_parameters(x)
    if operation in functions:
        if functions[operation][1] > 0:
            assert len(parameters) == functions[operation][1]
            return functions[operation][0](*parameters)
        else:
            assert len(parameters) >= -functions[operation][1]
            return functions[operation][0](parameters)
    else:
        raise ValueError('La sentencia no es válida')


if __name__ == '__main__':
    with open('../tests/logic_statements', 'r') as f:
        for sentencia in f.readlines():
            sentencia = str(sentencia).strip()
            try:
                print('============================================')
                print(sentencia)
                res = eval(sentencia)
                print(res)
            except Exception as myEx:
                print('ERROR', sentencia)
                print(myEx)
