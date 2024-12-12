from util import *
AES_modulus = BitVector(bitstring='100011011')
WORD_SIZE = 4 #BITS
MAX_ROUNDS = 0
KEY_LEN = 0 #WORDS
KEY_LEN_BYTES = 0 # Length of a key in bytes
key = [] # Original Key
N = 4 # Matrix Dim

roundKeys = []
reverseRoundKeys = []
rc = []

def genRC():
    rc[1] = 1
    for i in range(2, MAX_ROUNDS):
        if i > 1 and rc[i - 1] < 0x80:
            rc[i] = rc[i - 1] << 1
        else:
            rc[i] = (rc[i - 1] << 1) ^ 0x11B

def getRCon(round):
    return [BitVector(intVal=rc[round], size=8), 
            BitVector(hexstring="00"), 
            BitVector(hexstring="00"), 
            BitVector(hexstring="00")]

def arrayToMatrix(arr):
    matrix = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            matrix[i][j] = arr[j * N + i]
    return matrix

def matrixToArray(matrix):
    arr = [0 for _ in range(N * N)]
    for i in range(N):
        for j in range(N):
            arr[j * N + i] = matrix[i][j]
    return arr

def showArray(arr):
    for bv in arr:
        print(bv.get_bitvector_in_hex(), end = ' ')
    print()

def showBV(bv):
    print(bv.get_bitvector_in_hex(), end = ' ')

def showMatrix(matrix):
    for i in range(N):
        for j in range(N):
            showBV(matrix[i][j])
        print()

def circularByteShift(arr, right = 0):
    new_arr = arr.copy()
    n = len(new_arr)
    if right == 1:
        x = new_arr[n - 1]
        for i in range(n - 1, 0, -1):
            new_arr[i] = new_arr[i - 1]
        new_arr[0] = x
    else:
        x = new_arr[0]
        for i in range(1, n):
            new_arr[i - 1] = new_arr[i]
        new_arr[n - 1] = x
    return new_arr

def sboxLookUp(bv, inv = 0):
    int_val = bv.intValue()
    s = 0
    if not inv:
        s = Sbox[int_val]
    else:
        s = InvSbox[int_val]
    s = BitVector(intVal = s, size = 8)
    return s

def byteSubArray(arr):
    new_arr = arr.copy()
    n = len(new_arr)
    for i in range(n):
        new_arr[i] = sboxLookUp(new_arr[i])
    return new_arr

def byteSubMatrix(matrix, inv = 0):
    new_matrix = matrix.copy()
    for i in range(N):
        for j in range(N):
            new_matrix[i][j] = sboxLookUp(new_matrix[i][j], inv)
    return new_matrix

def getWords(key):
    w = [[BitVector(hexstring = "00") for _ in range(WORD_SIZE)] for _ in range(KEY_LEN)]
    for i in range(KEY_LEN):
        for j in range(WORD_SIZE):
            w[i][j] = key[i * WORD_SIZE + j]
    return w

def xorMatrix(m1, m2):
    m = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            m[i][j] = m1[i][j] ^ m2[i][j]
    return m

def xorArray(a1, a2):
    n = len(a1)
    ans = [0 for _ in range(n)]
    for i in range(0, n):
        ans[i] = a1[i] ^ a2[i]
    return ans

def multiplyBV(bv1, bv2):
    return bv1.gf_multiply_modular(bv2, AES_modulus, 8)

def multiplyMatrix(m1, m2):
    m = [[BitVector(hexstring="0") for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                m[i][j] ^= multiplyBV(m1[i][k], m2[k][j])
    return m

def getKey(words):
    n = WORD_SIZE * KEY_LEN
    key = [0 for _ in range(n)]
    for i in range(N):
        for j in range(N):
            key[i * N + j] = words[i][j]
    return key

def generateRoundKeys():
    genRC()
    k = getWords(key)
    w = [[BitVector(hexstring = "00") for _ in range(WORD_SIZE)] for _ in range(4 * MAX_ROUNDS)]
    for i in range(4 * MAX_ROUNDS):
        if i < KEY_LEN:
            w[i] = k[i]
        elif i >= KEY_LEN and i % KEY_LEN == 0:
            w[i] = xorArray(xorArray(w[i - KEY_LEN], byteSubArray(circularByteShift(w[i - 1]))), getRCon(i // KEY_LEN))
        elif i >= KEY_LEN and KEY_LEN > 6 and i % KEY_LEN == 4:
            w[i] = xorArray(w[i - KEY_LEN], byteSubArray(w[i - 1]))
        else:
            w[i] = xorArray(w[i - KEY_LEN], w[i - 1]) 

    rk = [0 for _ in range(MAX_ROUNDS)]
    for i in range(0, MAX_ROUNDS):
        rk[i] = getKey([w[i * 4], w[i * 4 + 1], w[i * 4 + 2], w[i * 4 + 3]])
    return rk

def shiftRow(matrix, inv = 0):
    new_matrix = matrix.copy()
    for i in range(N):
        for j in range(i):
            new_matrix[i] = circularByteShift(new_matrix[i], inv)
    return new_matrix

def performEncryptRound(round, prevStateMatrix):
    if (round == 0):
        return performEncryptRound(round + 1, xorMatrix(prevStateMatrix, arrayToMatrix(roundKeys[round])))
    
    stateMatrix = prevStateMatrix.copy()
    stateMatrix = byteSubMatrix(stateMatrix)
    stateMatrix = shiftRow(stateMatrix)

    if (round != MAX_ROUNDS - 1):
        stateMatrix = multiplyMatrix(Mixer, stateMatrix)
        stateMatrix = xorMatrix(stateMatrix, arrayToMatrix(roundKeys[round]))
        return performEncryptRound(round + 1, stateMatrix)
    
    stateMatrix = xorMatrix(stateMatrix, arrayToMatrix(roundKeys[round]))
    return matrixToArray(stateMatrix)

def performDecryptRound(round, prevStateMatrix):
    if (round == 0):
        return performDecryptRound(round + 1, xorMatrix(prevStateMatrix, arrayToMatrix(reverseRoundKeys[round])))
    
    stateMatrix = prevStateMatrix.copy()
    stateMatrix = shiftRow(stateMatrix, inv = 1)
    stateMatrix = byteSubMatrix(stateMatrix, inv = 1)
    stateMatrix = xorMatrix(stateMatrix, arrayToMatrix(reverseRoundKeys[round]))

    if (round != MAX_ROUNDS - 1):
        stateMatrix = multiplyMatrix(InvMixer, stateMatrix)
        return performDecryptRound(round + 1, stateMatrix)
    
    return matrixToArray(stateMatrix)

def AESEncrypt(txt):
    return performEncryptRound(0, arrayToMatrix(txt))

def AESDecrypt(cipherTxt):
    return performDecryptRound(0, arrayToMatrix(cipherTxt))

def partition(txt, n):
    chunks = []
    i = 0
    while i < len(txt):
        s = txt[i : i + n]
        while (len(s) < n):
            s += "\0"
        chunks.append(s)
        i += n
    return chunks

def strToBVArray(s):
    bvArray = [BitVector(intVal = ord(char), size = 8) for char in s]
    return bvArray

def bvArrayToStr(bvArray):
    s = [chr(bv.intValue()) for bv in bvArray]
    return ''.join(s)

def printHex(s):
    showArray(strToBVArray(s))

def AESEncryptText(txt):
    chunks = partition(txt, 16)
    output = ""
    for chunk in chunks:
        output += bvArrayToStr(AESEncrypt(strToBVArray(chunk)))
    return output

def AESDecryptText(txt):
    chunks = partition(txt, 16)
    output = ""
    for chunk in chunks:
        output += bvArrayToStr(AESDecrypt(strToBVArray(chunk)))
    return output

def aesInit(keyTxt, mode):
    global key, KEY_LEN, KEY_LEN_BYTES, MAX_ROUNDS, roundKeys, reverseRoundKeys, rc
    KEY_LEN = mode // 32
    KEY_LEN_BYTES = 4 * KEY_LEN
    if mode == 128:
        MAX_ROUNDS = 11
    elif mode == 192:
        MAX_ROUNDS = 13
    elif mode == 256:
        MAX_ROUNDS = 15
    
    if (len(keyTxt) > KEY_LEN_BYTES):
        keyTxt = keyTxt[:KEY_LEN_BYTES]
    while (len(keyTxt) < KEY_LEN_BYTES):
        keyTxt += "\0"
    
    rc = [0 for _ in range(MAX_ROUNDS)]
    key = strToBVArray(keyTxt)
    roundKeys = generateRoundKeys()
    reverseRoundKeys = roundKeys.copy()
    reverseRoundKeys.reverse()