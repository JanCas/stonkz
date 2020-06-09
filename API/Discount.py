# FCF= cash flow
# d = discount rate
# n = number of years
# g = growth rate
# p = P/E ratio
# e = earning available to common shares
def DCF(FCF, d, n, g, p, e):

    sum=0
    for t in range (1,n+1):
        FCF *= (1+g)
        sum += FCF/ ((1+d))**(t)
        #print (FCF/ ((1+d))**(t), sum)
    sum += (p * e) / ((1 + d)) ** (t)
    print(str(t) +'  ' +str (sum)+ '   '+ '   ' + str(FCF/((1+d))**(t))+ '    ')




DCF(12.03, 0.02, 5, 0.0188,21.49, 8.92)
