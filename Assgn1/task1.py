from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
import urllib.parse

def ECBencrypt(inputFile, outputFile, aesCipher):
    encrypting = True
    header = inputFile.read(54)
    outputFile.write(header)
    while encrypting:
        imgChunk = inputFile.read(16)
        if len(imgChunk) == 0 or len(imgChunk)%16 != 0:
            padding = 16 - len(imgChunk)
            if padding != 16:
                appendChar = chr(padding)
                imgChunk += padding * bytes(appendChar, 'utf-8')
            encrypting = False
        outputFile.write(aesCipher.encrypt(imgChunk))

def CBCencrypt(inputFile, outputFile, aesCipher):
    encrypting = True
    header = inputFile.read(54)
    outputFile.write(header)
    while encrypting:
        imgChunk = inputFile.read(16)
        if len(imgChunk) == 0 or len(imgChunk)%16 != 0:
            padding = 16 - len(imgChunk)
            if padding != 16:
                appendChar = chr(padding)
                imgChunk += padding * bytes(appendChar, 'utf-8')
            encrypting = False
        outputFile.write(aesCipher.encrypt(imgChunk))

def helperCBC(inputText, aesCipher):
    outputText = b''
    while len(inputText) > 0:
        imgChunk = inputText[:16]
        inputText = inputText[16:]
        outputText += aesCipher.encrypt(imgChunk.encode('UTF-8'))
    return outputText

def pkcs7(text, block_Size):
    output_text = ""
    if len(text) % block_Size != 0:
        delta = (len(text)//block_Size) + 1
        padding = (block_Size*delta) - len(text)
        appendChar = chr(padding)
        output_text = text + (appendChar * padding)
    if len(output_text) > 0:
        return output_text
    return text

def submit(data, aesCipher):
    data = data.replace('=', '%3D').replace(';', '%3B')
    UrlEncodedData = f"userid=456; userdata={data};session-id=31337"
    paddedData = pkcs7(UrlEncodedData, 16)
    encrypted_string = helperCBC(paddedData, aesCipher)
    return encrypted_string

def verify(data, aesCipher):
    
    decrypted_string = aesCipher.decrypt(data)

    return decrypted_string # result

def bit_flip(ecr_string):
    flip = "admin=true"
    newStr = str(ecr_string)[:-1]
    flipping = newStr[0:len(flip)]

    output = b''
    index = 0
    for ch in flipping:
        c = chr((ord(str(ch)) ^ ord(str(ch)) ^ ord (flip[index]))).encode('utf-8')
        output += c
        index += 1
    
    enc_string = ecr_string[0: len(ecr_string) - 10]
    enc_string += output
    return enc_string

if __name__ == "__main__":  
    key = get_random_bytes(16)
    iv = get_random_bytes(AES.block_size)
    if iv == key:
        iv = get_random_bytes(AES.block_size)
    with open("cp-logo.bmp", 'rb') as inputFile, open("ecbOutput.bmp", 'wb') as outputFile:
        aesCipher = AES.new(key, AES.MODE_ECB)
        ECBencrypt(inputFile, outputFile, aesCipher)
    with open("cp-logo.bmp", 'rb') as inputFile, open("cbcOutput.bmp", 'wb') as outputFile:
        aesCipher = AES.new(key, AES.MODE_CBC, iv)
        CBCencrypt(inputFile, outputFile, aesCipher)
    
    encrpAesCipher = AES.new(key, AES.MODE_CBC, iv)
    inputText = input("Enter Text: ")
    print()

    dt = submit(inputText, encrpAesCipher)
    print("Submit = " + str(dt))
    print()

    # print(len(dt))
    flipped = bit_flip(dt)
    
    decrpAesCipher = AES.new(key, AES.MODE_CBC, iv)
    dt = verify(flipped, decrpAesCipher)
    print(f"Verify = {dt}")
