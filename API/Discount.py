# FCF= cash flow
# d = discount rate
# n = number of years
# g= growth rate
def DCF(FCF, d, n, g,):

    sum=0
    for t in range (1,n+1):
        FCF *= (1+g)
        sum += FCF/ ((1+d))**(t)
        #print (FCF/ ((1+d))**(t), sum)



        print(str(t) +'  ' +str (sum)+ '   '+ '   ' + str(FCF)+ '    ' )



DCF(12.03, 0.05, 5, 0.0188,)
