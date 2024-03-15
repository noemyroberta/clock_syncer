def time_to_float(time_str):
    # Dividir a string nos ":" para obter as horas e minutos
    hours, minutes = map(int, time_str.split(':'))
    # Calcular o valor float equivalente em horas
    result = hours + minutes / 60
    return round(result, 2)

def float_to_time(float_value):
    # Obter as horas inteiras
    hours = int(float_value)
    # Obter os minutos arredondando para baixo e pegando o resto da divisão por 60
    minutes = int((float_value - hours) * 60)
    # Formatar o resultado no formato "HH:MM"
    return '{:02d}:{:02d}'.format(hours, minutes)