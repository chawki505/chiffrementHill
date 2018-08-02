import random


# calcule l'inverse de k mod n


def calcule_inverse_k_mod_n(k, n):
    for i in range(1, n):
        if (k * i) % n == 1:
            return i


# matrice 3x3
def calcule_inverse_matrice_mod_n(M, n):
    determinent = ((M[0] * M[4] * M[8]) -
                   (M[0] * M[5] * M[7]) -
                   (M[3] * M[1] * M[8]) +
                   (M[3] * M[2] * M[7]) +
                   (M[6] * M[1] * M[5]) -
                   (M[6] * M[2] * M[4]))

    # a b c    0 1 2
    # d e f => 3 4 5
    # g h i    6 7 8

    #       e       i      f      h     c      h     b       i     b      f      c      e
    key = [M[4] * M[8] - M[5] * M[7], M[2] * M[7] - M[1] * M[8], M[1] * M[5] - M[2] * M[4],
           # f      g      d      i     a      i      c      g     c      d      a      f
           M[5] * M[6] - M[3] * M[8], M[0] * M[8] - M[2] * M[6], M[2] * M[3] - M[0] * M[5],
           # d      h      e      g     b      g      a      h     a      e      b      d
           M[3] * M[7] - M[4] * M[6], M[1] * M[6] - M[0] * M[7], M[0] * M[4] - M[1] * M[3]]

    inv_determinent = calcule_inverse_k_mod_n(determinent, n)

    for i in range(0, len(key)):
        key[i] = key[i] * inv_determinent
        key[i] = key[i] % n
    return key


# pour generer la matrice de chiffrement 2X2 modulo n
def generation_matrice_chiffrement(n):
    M = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]
    while 1:
        for i in range(0, 9):
            M[i] = random.choice(range(1, n))

        determinent = ((M[0] * M[4] * M[8]) -
                       (M[0] * M[5] * M[7]) -
                       (M[3] * M[1] * M[8]) +
                       (M[3] * M[2] * M[7]) +
                       (M[6] * M[1] * M[5]) -
                       (M[6] * M[2] * M[4]))

        determinent = determinent % n

        inv_determinent = calcule_inverse_k_mod_n(determinent, n)

        if len(str(inv_determinent)) == 1:
            break

    return M


def getnum(lettre, alphabet):
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
    if tailleMessageClaire % 3 != 0:
        messageClaire += "X"

    # parcourire le msg pour le crypté
    for i in range(0, tailleMessageClaire, 3):
        codeP1 = getnum(messageClaire[i], alphabet)
        codeP2 = getnum(messageClaire[i + 1], alphabet)
        codeP3 = getnum(messageClaire[i + 2], alphabet)

        codeC1 = (key[0] * codeP1 + key[1] * codeP2 + key[2] * codeP3) % tailleAlphabet
        letC1 = getLettre(codeC1, alphabet)

        codeC2 = (key[3] * codeP1 + key[4] * codeP2 + key[5] * codeP3) % tailleAlphabet
        letC2 = getLettre(codeC2, alphabet)

        codeC3 = (key[6] * codeP1 + key[7] * codeP2 + key[8] * codeP3) % tailleAlphabet
        letC3 = getLettre(codeC3, alphabet)

        messageCrypte += letC1 + letC2 + letC3

    return messageCrypte


def dechiffrement(messageCrypte, keyChiffrement, alphabet):
    key = calcule_inverse_matrice_mod_n(keyChiffrement, len(alphabet))
    tailleAlphabet = len(alphabet)
    tailleMessageCrypte = len(messageCrypte)
    messageClaire = ""

    # test si la taile est un div 3
    if tailleMessageCrypte % 3 != 0:
        messageCrypte += "X"

    # parcourire le msg pour le decrypté
    for i in range(0, tailleMessageCrypte, 3):
        codeP1 = getnum(messageCrypte[i], alphabet)
        codeP2 = getnum(messageCrypte[i + 1], alphabet)
        codeP3 = getnum(messageCrypte[i + 2], alphabet)

        codeC1 = (key[0] * codeP1 + key[1] * codeP2 + key[2] * codeP3) % tailleAlphabet
        letC1 = getLettre(codeC1, alphabet)

        codeC2 = (key[3] * codeP1 + key[4] * codeP2 + key[5] * codeP3) % tailleAlphabet
        letC2 = getLettre(codeC2, alphabet)

        codeC3 = (key[6] * codeP1 + key[7] * codeP2 + key[8] * codeP3) % tailleAlphabet
        letC3 = getLettre(codeC3, alphabet)

        messageClaire += letC1 + letC2 + letC3

    return messageClaire.lower()


# matrice = [1, 3, 1,
#           1, 1, 0,
#          2, 9, 3]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
n = len(alphabet)
key = generation_matrice_chiffrement(n)

messageClaire = "donner votre message claire"
messageCrypte = chiffrement(messageClaire, key, alphabet)

print("matrice de chiffrement 3X3 : " + str(key))
print()
print("Message claire : " + messageClaire)
print("Message chiffrer : " + messageCrypte)
print()
print("redecryptage : " + dechiffrement(messageCrypte, key, alphabet))
