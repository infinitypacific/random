import math
def simpfrac(n,d):
    #dfac = [];
    #nfac = [];
    #for(let i=min(d,n)-1;i>1;i--): I forgot this was python...
    #math.ceil(math.sqrt(max(d,n))) idk
    
    #the PACIFIKY ALGORITHM (horrible)
    """
    for i in range(math.ceil(max(d,n)/2),1,-1):
        if(d%i == 0 and n%i == 0):
            return n/i,d/i
    """
    
    #Euclidian ALGORITHM (Smart)!!!
    flar = max(n,d)
    fmod = min(n,d)
    while(fmod != 0):
        tmod = flar%fmod
        flar = fmod
        fmod = tmod
    
    return n//flar,d//flar #WHY DOES PYTHON HAVE FLOOR DIVISION WHILE JS DOESn'T??

print(simpfrac(10,20))
print(simpfrac(72,30))
print(simpfrac(2,4))
print(simpfrac(100,333))