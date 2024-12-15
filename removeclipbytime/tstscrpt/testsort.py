bkp1 = 0;

def tsort(arr,carr=[]):
    #cocktail shaker ig
    indices = [0,0,0]
    if(arr[1] < arr[0]): 
        if(arr[2] < arr[0]):
            if(arr[2] < arr[1]):
                indices[0] = 2
                indices[1] = 1
            else:
                indices[0] = 1
                indices[1] = 2
        else:
            #arr[1] < arr[0] && arr[2] > arr[0] then arr[1] arr[0] arr[2]
            indices[0] = 1
            indices[2] = 2
    elif(arr[2] < arr[0]):
        #arr[1]>arr[0] && arr[2]<arr[0] && arr[2]<arr[1]
        #arr[1]>arr[0] && arr[2]<arr[0] && arr[2]>arr[1]
        #then arr[2] arr[0] arr[1]
        indices[0] = 2
        indices[2] = 1
    else:
        if(arr[2] < arr[1]):
            #arr[1]>arr[0] && arr[2]>arr[0] && arr[2]<arr[1]
            indices[1] = 2
            indices[2] = 1
        else:
            #arr[1]>arr[0] && arr[2]>arr[0] && arr[2]>arr[1]
            indices[1] = 1
            indices[2] = 2
    
    return ([arr[indices[0]],arr[indices[1]],arr[indices[2]]],[carr[indices[0]],carr[indices[1]],carr[indices[2]]]) if(len(carr) > 0) else ([arr[indices[0]],arr[indices[1]],arr[indices[2]]],indices)
        
    
def quickSort(arr,carr=[]):
    global bkp1
    if(len(carr) == 0):
        carr = list(range(len(arr)))
    if(len(arr) > 3):
        oindex = [len(arr)//2,len(arr)-1]
        pivsort,ipivsort = tsort([arr[0],arr[oindex[0]],arr[oindex[1]]],[carr[0],carr[oindex[0]],carr[oindex[1]]])
        #get pivot from a trisort of begin,mid,end
        arr[0] = pivsort[0]
        arr[oindex[1]] = pivsort[2]
        arr.pop(oindex[0])
        arr.append(pivsort[1])
        carr[0] = ipivsort[0]
        carr[oindex[1]] = ipivsort[2]
        carr.pop(oindex[0])
        carr.append(ipivsort[1])
        #print(carr)
        si = -1
        for i in range(len(arr)):
            if(arr[i]<=arr[oindex[1]]):
                si+=1
                if(i>si):
                    carr[i],carr[si] = carr[si],carr[i]
                    arr[i],arr[si] = arr[si],arr[i]
        print(arr);
        print(carr);
        input("Breakpoint1:"+str(bkp1));
        bkp1 += 1;
        arr[:si],carr[:si] = quickSort(arr[:si],carr[:si])
        arr[si+1:],carr[si+1:] = quickSort(arr[si+1:],carr[si+1:])
        return arr,carr
    elif(len(arr) == 3):
        return tsort(arr,carr)
    elif(len(arr) == 2):
        #print(carr)
        if(arr[0] > arr[1]):
            return [arr[1],arr[0]],[carr[1],carr[0]]
        else:
            return arr,carr
    elif(len(arr) == 1):
        return arr,carr
    else:
        return arr,[]
		
print(quickSort([4,1,2,5,6,0]))
print(tsort([3,1,2],[2,1,0]))
#^success
#Break cuz of duplicate?
print(quickSort([21,32,19,2,3,15,2,7,8],["1","2","3","4","5","6","7","8","9"]))