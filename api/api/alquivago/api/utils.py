def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    raise AssertionError("Invalid input for type", field)

def is_int(text):
    """convierte un numero en string en un int positivo,
    en caso contrario retorna None"""
    try:
        input = int(text)
        if input < 0:
            input = 0
    except (ValueError, TypeError):
        input = None
    return input
        

def tex_none(text):
    """
        separa varios nombes para formar una lista
    """
    if text is None:
        return None
    ret = [elemento for elemento in text.split(',') if elemento != ""]
    return(ret)


def chek_int(text):
    """
        separa una lista de numeros string(",") y evalua si son numeros,
        de lo contrario devuelve una lista con valores numero y None, (revisar eso)
    """
    numbers = tex_none(text)
    if numbers:
        ret = []
        for num in numbers:
            num = is_int(num)
            ret.append(num)
        numbers = ret
    return numbers


def sorting(text):
    """
        crea un dicionario con los nombres de las columnas y el orden (asendente o desendente)
        y lo prepara para el ordenamiento, si el valor no es valido no se crea el ordenamiento
    """
    sorts = tex_none(text)
    ret = {}
    if sorts:
        for s in sorts:
            s = s.split(':')
            if len(s) >= 2:
                s[1] = is_int(s[1])
                if s[1] is not None:
                    if s[1] > 1:
                        s[1] = 1
                    if s[1] == 0:
                        s[1] = -1
                    ret[s[0]] = s[1]
    return ret


def conversion():
    """return de conversion betwin two currencys"""
    return 40