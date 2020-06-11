def EV(n, g, wacc, starting_fcf, cash, debt, shares_outstanding):
    entval = starting_fcf
    for x in range(1, n + 1):
        entval += (starting_fcf * (1 + g) ** x) / ((1 + wacc) ** x)
    entval += (starting_fcf * ((1 + g) ** (n + 1))) / (1 + wacc)

    eqval = entval + cash - debt
    PricePerShare = eqval / shares_outstanding

    return entval, eqval, PricePerShare

print(EV(4, .1, .07, 10, 100, 50, 100))
