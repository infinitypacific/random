try:
    from lxml import etree as XMLTree
except ImportError:
    import xml.etree.ElementTree as XMLTree
import argparse,math

def getTime(s):
    dem,num = 0,0
    for i in range(len(s)):
        if(s[i] == "/"):
            num = int(s[:i])
            den = int(s[i+1:-1])
            break;
    return num,den
	
def getFormat(formats,id):
    for i in range(len(formats)):
        if(formats[i].attrib["id"] == id):
            return formats[i]
            
    return None
    
def normalizeTime(s,fps):
    durnum,durden = getTime(s)
    return durnum*(fps/durden)

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
        
#Implemented this cuz i'm stressed
def simpfrac(n,d):
    flar = max(n,d)
    fmod = min(n,d)
    while(fmod != 0):
        tmod = flar%fmod
        flar = fmod
        fmod = tmod
    
    return n//flar,d//flar

def quickSort(arr,carr=[]):
    #In testing
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

parser = argparse.ArgumentParser()
parser.add_argument("file",help='The filename of the timeline',nargs='+',type=str)
parser.add_argument("-t","--time",help='The time to cut (number)',nargs='?',type=float)
parser.add_argument("-l","--long",help='Cut longer than the time?',nargs='?',default=False,type=bool)
parser.add_argument("-f","--frame",help='Interpret time as frame amount (will be floored)',nargs='?',default=False,type=bool)
parser.add_argument("-r","--ripple",help='Ripple cut? (Default true)',nargs='?',default=True,type=bool)
args = parser.parse_args()
#input(args.ripple) #ohh so just adding (-f + whatever) enables it
#FCPFile = []

if(args.time is None):
    raise Exception("Missing time flag! (Use -t or -h)")
time = args.time

for i in range(len(args.file)):
    if(args.file[i][-7:] != ".fcpxml"):
        raise Exception("File is not fcpxml!")
    #FCPFile.append(args.file[i])

for i in range(len(args.file)):
    try:
        tree = XMLTree.parse(args.file[i])
    except:
        raise Exception("File IOError! "+args.file[i])
    root = tree.getroot()
    if(root.attrib["version"] != "1.8"):
        raise Exception("Invalid version, expecting 1.8")
    lib = root.find('library')
    formats = root.find('resources').findall('format')
    events = lib.findall('event')
    for j in range(len(events)):
        #print(elm.attrib["test"])
        #elm.attrib["test"] = "okay"
        projects = events[j].findall('project')
        for k in range(len(projects)):
            sequence = projects[k].find("sequence")
            fpsn,fpsd = getTime(getFormat(formats,sequence.attrib['format']).attrib['frameDuration'])
            fps = fpsd/fpsn
            #Normalize everything to fps because dividing to seconds can result in floating point errors and inconsistencies
            #time = numer*(fps/denom)
            #Except fps needs to be int upon used in attributes
            ntime = time
            if(not args.frame):
                ntime *= fps
            #input(ntime);
            print("Project "+projects[k].attrib['name']+" fps: "+str(fps))
            if(sequence is None):
                raise Exception("Project "+projects[k].attrib['name']+" is missing a sequence!")
            spine = sequence.find('spine')
            if(spine is None):
                raise Exception("Project "+projects[k].attrib['name']+" is missing a spine!")
            lanemtx = []
            lanemtxid = []
            for l in range(len(spine)-1,-1,-1):
                #print(l)
                match spine[l].tag:
                    case ("clip" | "video" | "asset-clip" | "title" | "ref-clip"):
                        pndur = normalizeTime(spine[l].attrib["duration"],fps)
                        pnoff = normalizeTime(spine[l].attrib["offset"],fps)
                        pnstt = normalizeTime(spine[l].attrib["start"],fps)
                        #print(ndur)
                        premflag = (args.long and ntime < pndur) or (not args.long and ntime >= pndur)
                        #Collect child clips to keep if parent is removed
                        for m in range(len(spine[l])):
                            match spine[l][m].tag:
                                case ("clip" | "video" | "asset-clip" | "title" | "ref-clip"):
                                    if("lane" not in spine[l][m].keys()): continue
                                    rlane = int(spine[l][m].attrib["lane"])
                                    if(rlane in lanemtxid):
                                        lanemtx[lanemtxid.index(rlane)].append(spine[l][m]);
                                    else:
                                        lanemtxid.append(rlane)
                                        lanemtx.append([spine[l][m]])
                                    
                                    #normalizing offset to be subtracted from recieving start spine[l][m].offset = (spine[l][m].offset-reciever.offset)+reciever.start 
                                    #spine[l][m].offset = (spine[l][m].offset-spine[l].start)+spine[l].offset
                                    cnoff = (normalizeTime(spine[l][m].attrib["offset"],fps)-pnstt)+pnoff
                                    #sn,sd = simpfrac(int(cnoff),int(fps))
                                    #spine[l][m].attrib["offset"] = str(sn) + "/" + str(sd) + "s";
                                    spine[l][m].attrib["offset"] = str(cnoff)
                                    print(spine[l][m].attrib["duration"] + ": " + str(cnoff))
                                    if(premflag):
                                        spine[l].remove(spine[l][m])
                        if(premflag):
                            #print("RemoveClip")
                            #move front clips back
                            if(args.ripple):
                                for m in range(l+1,len(spine)):
                                    noff = normalizeTime(spine[m].attrib["offset"],fps)
                                    noff -= pndur
                                    sn,sd = simpfrac(int(noff),int(fps))
                                    #print(sn)
                                    #print(sd)
                                    spine[m].attrib["offset"] = str(sn) + "/" + str(sd) + "s"
                                    #Audio child tags seems to follow the video's offset so ye
                            spine.remove(spine[l])
                    case "gap":
                        pnoff = normalizeTime(spine[l].attrib["offset"],fps)
                        pnstt = normalizeTime(spine[l].attrib["start"],fps)
                        for m in range(len(spine[l])):
                            if("lane" not in spine[l][m].keys()): continue
                            match spine[l][m].tag:
                                case ("clip" | "video" | "asset-clip" | "title" | "ref-clip"):
                                    rlane = int(spine[l][m].attrib["lane"])
                                    if(rlane in lanemtxid):
                                        lanemtx[lanemtxid.index(rlane)].append(spine[l][m]);
                                    else:
                                        lanemtxid.append(rlane)
                                        lanemtx.append([spine[l][m]])
                                    #spine[l].remove(spine[l][m])
                                    #print("hello")
                                    cnoff = (normalizeTime(spine[l][m].attrib["offset"],fps)-pnstt)+pnoff
                                    #sn,sd = simpfrac(int(cnoff),int(fps))
                                    #spine[l][m].attrib["offset"] = str(sn) + "/" + str(sd) + "s";
                                    print(cnoff)
                                    spine[l][m].attrib["offset"] = str(cnoff)
            #Quicksort for edge cases:
            durmtx = []
            #print(lanemtx)  
            for l in range(len(lanemtx)):
                durmtx.append([]) #Append an empty list for each lane cuz python stupid
                for m in range(len(lanemtx[l])):
                    #durmtx[l].append(normalizeTime(lanemtx[l][m].attrib["duration"],fps))
                    durmtx[l].append(float(lanemtx[l][m].attrib["offset"]))
                durmtx[l],lanemtx[l] = quickSort(durmtx[l],lanemtx[l]);
            #print(lanemtx)
            if(len(spine) == 0):
                #Append gap to hold child clips if nothing in spine
                spine.append(XMLTree.Element("gap", attrib={"start":"3600/1s","name":"Gap","offset":"3600/1s","duration":"0/1s"}))
            lazyelm = spine[0]
            #print(len(lanemtx))
            for l in range(len(lanemtx)-1,-1,-1):
                for m in range(len(lanemtx[l])-1,-1,-1):
                    ndur = normalizeTime(lanemtx[l][m].attrib["duration"],fps)
                    #print("ndur" + str(ndur));
                    #print("durmtx" + str(durmtx[l][m]));
                    #print(lanemtx[l][m])
                    childclippar = lanemtx[l][m].getparent()
                    #print(childclippar)
                    #if((args.long and ntime < durmtx[l][m]) or (not args.long and ntime >= durmtx[l][m])):
                    if((args.long and ntime < ndur) or (not args.long and ntime >= ndur)):
                        print("Removed this one: " + str(ndur))
                        #print("Remove: " + str(l) + ":" + str(m))
                        #print("RemoveClip")
                        #child offsets are relative to parent start
                        if(childclippar is not None):
                            childclippar.remove(lanemtx[l])
                        if(args.ripple):
                            for n in range(m+1,len(lanemtx[l])):
                                #Doesn't work because sorted by duration (why did I do that? i forgor)
                                #noff = normalizeTime(lanemtx[l][n].attrib["offset"],fps)
                                #print("erm" + lanemtx[l][n].attrib["offset"])
                                #noff = durmtx[l][n]
                                #noff -= durmtx[l][m]
                                #noff -= ndur
                                #sn,sd = simpfrac(int(noff),int(fps))
                                #lanemtx[l][n].attrib["offset"] = str(int(sn)) + "/" + str(int(sd)) + "s"
                                print(lanemtx[l][n].attrib["duration"] + ": " + str(durmtx[l][n]))
                                durmtx[l][n] -= ndur
                        #Repeat assign prob!
                        lanemtx[l].pop(m)
                        durmtx[l].pop(m)
                    else:
                        #print(childclippar)
                        if(childclippar is None):
                            lazyelm.append(lanemtx[l][m])
            
            for l in range(len(lanemtx)):
                for m in range(len(lanemtx[l])):
                    print("Correct: " + str(l) + ":" + str(m))
                    #this is where the error is prob
                    childclippar = lanemtx[l][m].getparent()
                    noff = (durmtx[l][m]-normalizeTime(childclippar.attrib["offset"],fps))+normalizeTime(childclippar.attrib["start"],fps)
                    sn,sd = simpfrac(int(noff),int(fps))
                    lanemtx[l][m].attrib["offset"] = str(int(sn)) + "/" + str(int(sd)) + "s"
    #FCPFile[i].truncate(0)
    #FCPFile[i].seek(0)
    #FCPFile[i].close()
    tree.write(args.file[i][:-7] + " - removed.fcpxml")