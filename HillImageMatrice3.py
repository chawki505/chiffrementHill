import random
import numpy as np
from PIL import Image as img

modulo = 256


# calcule l'inverse de k mod n
def calcule_inverse_k_mod_n(k: int) -> int:
    for i in range(1, modulo):
        if (i % 2 != 0) and (i % 13 != 0) and (k * i) % modulo == 1:
            return i


# calcule l'inverse d'une matrice 3X3
def calcule_inverse_matrice_mod_n(M):
    determinent = ((M[0] * M[4] * M[8]) -
                   (M[0] * M[5] * M[7]) -
                   (M[3] * M[1] * M[8]) +
                   (M[3] * M[2] * M[7]) +
                   (M[6] * M[1] * M[5]) -
                   (M[6] * M[2] * M[4]))

    # a b c    0 1 2
    # d e f => 3 4 5 =>
    # g h i    6 7 8

    #       e       i      f      h     c      h     b       i     b      f      c      e
    matrice_inverse = [M[4] * M[8] - M[5] * M[7], M[2] * M[7] - M[1] * M[8], M[1] * M[5] - M[2] * M[4],
                       # f      g      d      i     a      i      c      g     c      d      a      f
                       M[5] * M[6] - M[3] * M[8], M[0] * M[8] - M[2] * M[6], M[2] * M[3] - M[0] * M[5],
                       # d      h      e      g     b      g      a      h     a      e      b      d
                       M[3] * M[7] - M[4] * M[6], M[1] * M[6] - M[0] * M[7], M[0] * M[4] - M[1] * M[3]]

    inv_determinent = calcule_inverse_k_mod_n(determinent)

    for i in range(len(matrice_inverse)):
        matrice_inverse[i] = matrice_inverse[i] * inv_determinent % modulo

    return matrice_inverse


# pour generer la matrice de chiffrement 3X3 modulo n
def generation_matrice_chiffrement():
    M = [1, 1, 1,
         1, 1, 1,
         1, 1, 1]
    while 1:
        for i in range(len(M)):
            M[i] = random.choice(range(1, modulo))

        determinent = ((M[0] * M[4] * M[8]) -
                       (M[0] * M[5] * M[7]) -
                       (M[3] * M[1] * M[8]) +
                       (M[3] * M[2] * M[7]) +
                       (M[6] * M[1] * M[5]) -
                       (M[6] * M[2] * M[4]))

        determinent = determinent % modulo

        inv_determinent = calcule_inverse_k_mod_n(determinent)

        if inv_determinent:
            break

    return M


def chiffrementImage(image_claire, key):
    image_claire = image_claire.convert("RGB")

    imageArray = np.asarray(image_claire)
    imageArray.setflags(write=True)

    (largeur, hauteur) = image_claire.size

    # parcourir les pixel pour crypté
    for x in range(hauteur):
        for y in range(largeur):
            pixel = imageArray[x, y]
            codeR = (key[0] * pixel[0] + key[1] * pixel[1] + key[2] * pixel[2]) % modulo

            codeG = (key[3] * pixel[0] + key[4] * pixel[1] + key[5] * pixel[2]) % modulo

            codeB = (key[6] * pixel[0] + key[7] * pixel[1] + key[8] * pixel[2]) % modulo

            imageArray[x, y] = (codeR, codeG, codeB)

    image_crypte = img.fromarray(imageArray)
    image_crypte = image_crypte.convert("RGB")

    return image_crypte


def dechiffrementImage(image_crypte, keyChiffrement):
    image_crypte = image_crypte.convert("RGB")

    key = calcule_inverse_matrice_mod_n(keyChiffrement)

    imageArray = np.asarray(image_crypte)
    imageArray.setflags(write=True)

    (largeur, hauteur) = image_crypte.size


    # parcourir les pixels pour crypté
    for x in range(hauteur):
        for y in range(largeur):
            pixel = imageArray[x, y]

            codeR = (key[0] * pixel[0] + key[1] * pixel[1] + key[2] * pixel[2]) % modulo
            codeG = (key[3] * pixel[0] + key[4] * pixel[1] + key[5] * pixel[2]) % modulo
            codeB = (key[6] * pixel[0] + key[7] * pixel[1] + key[8] * pixel[2]) % modulo

            imageArray[x, y] = (codeR, codeG, codeB)

    image_claire = img.fromarray(imageArray)
    image_claire = image_claire.convert("RGB")
    return image_claire


print("lecture image")
image = img.open("img/logoNike.png")

# image.show()
#
print("generation cle")
key = generation_matrice_chiffrement()
print(key)
#
print("crypter image")
imageCrypte = chiffrementImage(image, key)
# imageCrypte.show()
#
print("save image crypter")
imageCrypte.save("crypter.png")
#
print("decryptage image crypter")
imageDecrypte = dechiffrementImage(imageCrypte, key)
# imageDecrypte.show()

print("save image decrypter")
imageDecrypte.save("decrypter.png")
