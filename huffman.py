test_file = "test.txt"
formatExtension = "hm"
readSize = 1

def compress(fileName):
    
    #Add in check that the file exists.
    
    #new file name (make optional in future to add custom new name)
    newName = "".join(fileName.split(".")[:-1]) + "." + formatExtension 
    
    #intializes a list to store characters (bytes, but it's easier to think), and their frequency
    charMap = []
    
    #opens file, and then reads the first byte
    with open(fileName, "rb") as file:
        byte_ = file.read(readSize) #maybe increase size and add for b in byte_?
        #while there are bytes it checks if char (/byte) is already in the list, if so add to it's frequency, if not adds it to list with the value of 1
        while byte_:
            chars = [c[0] for c in charMap]
            if byte_ in chars: charMap[chars.index(byte_)][1] += 1
            else: charMap.append([byte_, 1])
            
            #read next
            byte_ = file.read(readSize)
    
    
    # Idea to indicate the end of the file, because the compressed output might need to have added filler to fill an whole byte (min write size)
    #   Maybe do some math or smth if this is worth it?
        #Ending character.
    #charMap.append(["RM", 1])


    #using huffman coding makes the binary tree representation.
    ogCharmapLen = len(charMap) #stores for later use
    while len(charMap) != 2: 
        # keeps making the tree until it only contains two options
        charMap = sorted(charMap, key=lambda e: e[1])
        # sorts by e[1], because the frequency of the char/byte/node is stored at index 1 
        node = [[], 0]
        # creates the next node with proper format
        
        # takes the two smallest and combines them
        for n in range(2):
            node[0].append(charMap[n])
            node[1] += charMap[n][1]
        charMap = charMap[2:] ; charMap.append(node)
    
    # shows what is stored in the tree at an address, that can be pseudo binary
    def moveTo(addr):
        tmpMap = charMap[addr[0]] # due to formating reasons [0] needs to be done, so the frequency isn't picked
        for i in addr[1:]:
            tmpMap = tmpMap[0][i] # same here as ^
        return(tmpMap)
            

    #assings bytes
    byteMap = [] # will include [char, byte]
    curAddr = [0] # intializes the address to a value that will work.
    
    # this function will walk the tree, and assign the compressed representations of each byte
    while True: #len(byteMap) != ogCharmapLen:
        curData = moveTo(curAddr)
        if type(curData[0]) != list: # == bytes
            #2nd index could be changed, to just return curAddr, and leave out len, but for some reason it doesn't work, as it takes repeat values for no apparent reason.
            byteMap.append(
                [curData[0], 
                 sum([curAddr[i] << i for i in range(len(curAddr))]), #.to_bytes(len(curAddr) // 8 +1, byteorder = "big")
                 len(curAddr)]
                )
            if len(byteMap) == ogCharmapLen: break
            
            
            if curAddr[-1] == 0: curAddr[-1] = 1
            else:
                curAddr = curAddr[:-1]
                while True: #curAddr[-1] != 1: 
                    if curAddr[-1] == 0: curAddr[-1] = 1 ; break
                    else: curAddr = curAddr[:-1] 
        else: curAddr.append(0)

    #     #debug
    # for indx, val in enumerate(byteMap):
    #     #print(f"{indx}:\t {bits2form(val[1])}, {val[0]}")
    #     print(f"{indx}:\t {val}")


    # Rest does not work

        #make the bytemap into bytes (HEH)
            #MAKE A MORE OPTIMAL DICT LATER!


        #overwrite / create file
    with open(newName, "w") as file: pass

        #write in a headerfile
    info = b's45 [v0.1] [RM_]'
    with open(newName, "wb") as file:
        file.write(info)




        #create & write the binary representation.
    bitMask8F = (1 << 8) -1
    with open(fileName, "rb") as rFile:
        with open(newName, "a+b") as wFile:
            byte_ = rFile.read(1)
            writeByte = 0; writeByteLen = 0
            while byte_:
                curByte = byteMap[[i[0] for i in byteMap].index(byte_)][1:]    
                writeByte += curByte[0] << writeByteLen
                
                while writeByteLen >= 8:
                    #do the writing
                    imWrite = (writeByte & bitMask8F)
                    imWrite = imWrite.to_bytes(1, byteorder = "big")
                    wFile.write(imWrite)
                    #do clean up
                    writeByte >>= 8
                    writeByteLen -= 8
                
                writeByteLen += curByte[1]
                
                #read next
                byte_ = rFile.read(1)
    #add in the remiander in the buffer, and acknowledge the buffer length.


    #temp dict writefile
    import json
    d = {"data" : [[int.from_bytes(i[0], byteorder="big"), i[1], i[2]] for i in byteMap]}
    #print(d)
    with open("test.json", "w") as file:
        json.dump(d, file)
    
def decompress(fileName):
    newFile = "test2.txt"
    
    #get dict:
    import json
    with open("test.json", "r") as file:
        byteMap = json.load(file)["data"]
    byteMap = [ [i[0].to_bytes(1, byteorder = "big"), i[1], i[2]] for i in byteMap]
    bytemap = sorted(byteMap, key=lambda x: x[2])
    
    with open(fileName, "rb") as rFile:
        with open(newFile, "a+b") as wFile:
            byte_ = rFile.read(16); byte_ = rFile.read(1)
            curByte = 0; curByteLen = 0
    
            while byte_:
                curByte += int.from_bytes(byte_, byteorder="big") << curByteLen
                curByteLen += 8
                
                for i in byteMap:
                    if (curByte & ( (1 << i[2]) - 1 )) ^ i[1] == 0 and i[2] <= curByteLen:
                        wFile.write(i[0])
                        curByte >>= i[2]
                        curByteLen -= i[2]
                        #input("")
                            
                byte_ = rFile.read(1)
        
        # canGo = True
        # while canGo:
        #     for i in byteMap:
        #         if (curByte & ( (1 << i[2]) - 1 )) ^ i[1] == 0:
        #             print(i)
        #             curByte >>= i[2]
                    
        #             input()
            
compress(test_file)
decompress("test.hm")
