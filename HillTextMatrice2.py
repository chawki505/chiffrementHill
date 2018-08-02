import random


# calcule l'inverse de k mod n
def calcule_inverse_k_mod_n(k, n):
    for i in range(1, n):
        if (k * i) % n == 1:
            return i


# calculer l'inverse d'une matrice
def calcule_inverse_matrice_mod_n(matrice, n):
    determinent = matrice[0] * matrice[3] - matrice[1] * matrice[2]
    key = [matrice[3], -matrice[1], -matrice[2], matrice[0]]

    inv_determinent = calcule_inverse_k_mod_n(determinent, n)

    for i in range(0, len(key)):
        key[i] = key[i] * inv_determinent
        key[i] = key[i] % n
    return key


# pour generer la matrice de chiffrement 2X2 modulo n
def generation_matrice_chiffrement(n):
    while 1:
        a = random.choice(range(1, n))
        b = random.choice(range(1, n))
        c = random.choice(range(1, n))
        d = random.choice(range(1, n))

        determinent = (a * d - b * c) % n

        inv_determinent = calcule_inverse_k_mod_n(determinent, n)

        if len(str(inv_determinent)) == 1:
            break
    return [a, b, c, d]


def getnum(lettre, alphabet):
    lettre = lettre.upper()
    for i in range(0, len(alphabet)):
        if lettre == alphabet[i]:
            return int(i)


def getLettre(num, alphabet):
    return alphabet[num]


def chiffrement(messageClaire, key, alphabet):
    messageClaire = messageClaire.upper()  # passage majusule
    messageClaire = messageClaire.replace(" ", "")  # suprimer les espaces

    messageCrypte = ""

    tailleAlphabet = len(alphabet)
    tailleMessageClaire = len(messageClaire)

    # test si la taile est impaire
    if tailleMessageClaire % 2 != 0:
        messageClaire += "X"

    # parcourire le msg pour le crypté
    for i in range(0, tailleMessageClaire, 2):
        codeP1 = getnum(messageClaire[i], alphabet)
        codeP2 = getnum(messageClaire[i + 1], alphabet)

        codeC1 = (key[0] * codeP1 + key[1] * codeP2) % tailleAlphabet
        letC1 = getLettre(codeC1, alphabet)

        codeC2 = (key[2] * codeP1 + key[3] * codeP2) % tailleAlphabet
        letC2 = getLettre(codeC2, alphabet)

        messageCrypte += letC1 + letC2

    return messageCrypte


def dechiffrement(messageCrypte, keyChiffrement, alphabet):
    key = calcule_inverse_matrice_mod_n(keyChiffrement, len(alphabet))
    tailleAlphabet = len(alphabet)
    tailleMessageCrypte = len(messageCrypte)
    messageClaire = ""

    # test si la taile est impaire
    if tailleMessageCrypte % 2 != 0:
        messageCrypte += "X"

    # parcourire le msg pour le decrypté
    for i in range(0, tailleMessageCrypte, 2):
        codeP1 = getnum(messageCrypte[i], alphabet)
        codeP2 = getnum(messageCrypte[i + 1], alphabet)

        codeC1 = (key[0] * codeP1 + key[1] * codeP2) % tailleAlphabet
        letC1 = getLettre(codeC1, alphabet)

        codeC2 = (key[2] * codeP1 + key[3] * codeP2) % tailleAlphabet
        letC2 = getLettre(codeC2, alphabet)

        messageClaire += letC1 + letC2

    return messageClaire.lower()


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
n = len(alphabet)
# key = generation_matrice_chiffrement(n)
key = [9, 4, 5, 7]

messageClaire = "JEVOUSDISOUI"
messageCrypte = chiffrement(messageClaire, key, alphabet)
messageDecrypte = dechiffrement(messageCrypte, key, alphabet)

for i in range(len(messageCrypte)):
    print(str(getnum(messageCrypte[i], alphabet)) + " " + messageCrypte[i])

print("fin")

for i in range(len(messageDecrypte)):
    print(str(getnum(messageDecrypte[i], alphabet)) + " " + messageDecrypte[i])

print("matrice de chiffrement 2X2 : " + str(key))
print()
print("Message claire : " + messageClaire)
print("Message chiffrer : " + messageCrypte)
print()
print("redecryptage : " + messageDecrypte)
