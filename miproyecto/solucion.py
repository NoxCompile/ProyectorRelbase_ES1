def decidir(stock_actual, ventas_esperadas):
    if stock_actual < 0 or ventas_esperadas < 0:
        return "Invalido"
    elif stock_actual >= ventas_esperadas:
        return "Optimo"
    elif stock_actual >= (ventas_esperadas / 2):
        return "Alerta"
    else:
        return "Critico"