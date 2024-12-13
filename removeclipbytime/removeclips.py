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
        
    
def quickSort(arr,carr=[]):
    if(len(carr) == 0):
        carr = list(range(len(arr)))
    if(len(arr) > 3):
        oindex = [0,len(arr)//2,len(arr)-1]
        pivsort,ipivsort = tsort([arr[0],arr[oindex[1]],arr[oindex[2]]])
        arr[0] = pivsort[0]
        arr[oindex[2]] = pivsort[2]
        arr.pop(oindex[1])
        arr.append(pivsort[1])
        carr[0] = oindex[ipivsort[0]]
        carr[oindex[2]] = oindex[ipivsort[2]]
        carr.pop(oindex[1])
        carr.append(oindex[ipivsort[1]])
        #print(carr)
        si = -1
        for i in range(len(arr)):
            if(arr[i]<=arr[oindex[2]]):
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
parser.add_argument("-t","--time",help='The time to cut',nargs='?',type=float)
parser.add_argument("-l","--long",help='Cut longer than the time?',nargs='?',default=False,type=bool)
parser.add_argument("-f","--frame",help='Interpret time as frame amount (will be floored)',nargs='?',default=False,type=bool)
args = parser.parse_args()
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
            if(not args.frame):
                time *= fps
            
            print("Project "+projects[k].attrib['name']+" fps: "+str(fps))
            if(sequence is None):
                raise Exception("Project "+projects[k].attrib['name']+" is missing a sequence!")
            spine = sequence.find('spine')
            if(spine is None):
                raise Exception("Project "+projects[k].attrib['name']+" is missing a sequence!")
            lanemtx = []
            for l in range(len(spine)-1,-1,-1):
                print(l)
                match spine[l].tag:
                    case ("clip" | "video" | "asset-clip" | "title" | "ref-clip"):
                        ndur = normalizeTime(spine[l].attrib["duration"],fps)
                        print(ndur)
                        if((args.long and time < ndur) or (not args.long and time >= ndur)):
                            print("RemoveClip")
                            for m in range(l+1,len(spine)):
                                noff = normalizeTime(spine[m].attrib["offset"],fps)
                                noff -= ndur
                                spine[m].attrib["offset"] = str(math.floor(noff)) + "/30s"
                                #Audio child tags seems to follow the video's offset so ye
                            for m in range(len(spine[l])):
                                if("lane" not in spine[l][m].keys()): continue
                                match spine[l][m].tag:
                                    case ("clip" | "video" | "asset-clip" | "title" | "ref-clip"):
                                        rlane = int(spine[l][m].attrib["lane"])
                                        for n in range(rlane-len(lanemtx)): lanemtx.append([])
                                        lanemtx[rlane-1].append(spine[l][m])
                            spine.remove(spine[l])
            #Quicksort for edge cases:
            durmtx = []
            for l in range(len(lanemtx)):
                durmtx.append([])
                for m in range(len(lanemtx[l])):
                    durmtx[l].append(normalizeTime(lanemtx[l][m].attrib["duration"],fps))
            print(lanemtx)
            if(len(spine) == 0):
                spine.append(XMLTree.Element("gap", attrib={"start":"3600/1s","name":"Gap","offset":"3600/1s","duration":"0/1s"}))
            lazyelm = spine[0]
            for l in range(len(lanemtx)):
                for m in range(len(lanemtx[l])):
                    ndur = normalizeTime(lanemtx[l][m].attrib["duration"],fps)
                    print(ndur)
                    if((args.long and time < ndur) or (not args.long and time >= ndur)):
                        print("RemoveClip")
                        for n in range(m+1,len(lanemtx[l])):
                            noff = normalizeTime(lanemtx[l][n].attrib["offset"],fps)
                            noff -= ndur
                            spine[m].attrib["offset"] = str(math.floor(noff)) + "/30s"
                            #Audio child tags seems to follow the video's offset so ye
                    else:
                        lazyelm.append(lanemtx[l][m])
    
    #FCPFile[i].truncate(0)
    #FCPFile[i].seek(0)
    #FCPFile[i].close()
    tree.write(args.file[i][:-7] + " - removed.fcpxml")