def encryp(password): 
    kata = 'abcdefghijklmnopqrstuvwxyz'
    translated = ''
    for symbol in password:
        if symbol in kata:
            num = kata.find(symbol)
            num = num + 3
        if num >= len(kata):
            num -= len(kata)
        translated += kata[num]
    return translated
def decryp(password): 
    kata = 'abcdefghijklmnopqrstuvwxyz'
    translated = ''
    for symbol in password:
        if symbol in kata:
            num = kata.find(symbol)
            num = num - 3
        if num >= len(kata):
            num -= len(kata)
        translated += kata[num]
    return translated