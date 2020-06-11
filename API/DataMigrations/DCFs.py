def EV(n, g, wacc, starting_fcf, cash, debt, shares_outstanding):
    entval = starting_fcf
    for x in range(1, n + 1):
        entval += ((starting_fcf * (1 + g) ** x) / ((1 + wacc) ** x))
        #print((starting_fcf * (1 + g) ** x))
        finalfcf = (starting_fcf * (1 + g) ** x)

    entval += (finalfcf * (1 + g))/(wacc - g)
    #entval += (starting_fcf * ((1 + g) ** (n + 1))) / (wacc - g)

    eqval = entval + cash - debt
    PricePerShare = eqval / shares_outstanding

    return entval, eqval, PricePerShare

print(EV(4, .1147, .07, 58.9, 100.5, 108.06, 4.33))
#print(EV(4,.0187, .08, 8.42, 11.18, 42.77, 4.29))
#print(EV(4, .1, .15, 10, 100, 50, 100))