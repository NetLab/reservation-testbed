def MakeHeader(commentChar, fillChar, header, length, endChar, hasEnd = False, caps = False):
    textHeader = [fillChar] * length
    print(len(textHeader))
    comCharLen = len(commentChar)
    i = 0
    while i < comCharLen:
        textHeader[i] = commentChar[i]
        i += 1
    textHeader[i] = ' '     # Space between comment char and first fill char

    if hasEnd:
        endCharLen = len(endChar)
        i = 0
        while i < endCharLen:
            textHeader[-(i + 1)] = endChar[-(i+1)]
            i += 1
            textHeader[-(i + 1)] = ' '  # Space between end char and last fill char

    if caps:
        header = header.upper()

    headerLen = len(header)
    spaceOffset = 1
    sideLen = int((length - headerLen*2 - spaceOffset)/2)

    i = 0
    while i < headerLen * 2:
        textHeader[sideLen + i] = ' '
        textHeader[sideLen + i + 1] = header[int(i/2)]
        i += 2
    textHeader[sideLen + i] = ' '
    print(''.join(textHeader))

MakeHeader('#', '=', "Generation", 80, ' ')