import random
import numpy as np
from PIL import Image as img
from resizeimage import resizeimage

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

    matrice_inverse = [M[4] * M[8] - M[5] * M[7], M[2] * M[7] - M[1] * M[8], M[1] * M[5] - M[2] * M[4],
                       M[5] * M[6] - M[3] * M[8], M[0] * M[8] - M[2] * M[6], M[2] * M[3] - M[0] * M[5],
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
    (largeur, hauteur) = image_claire.size  # get size image
    while largeur % 3 != 0:  # ajouter des pixels si la taille en longeur ne corespond pas a la cle de chiffrement
        image_claire = resizeimage.resize_crop(image_claire, (largeur + 1, hauteur))
        image_claire = image_claire.convert("RGB")
        largeur = largeur + 1

    # get image array
    imageArray = np.asarray(image_claire)
    imageArray.setflags(write=True)

    # get color array
    rouge = np.asarray(imageArray[:, :, 0])
    vert = np.asarray(imageArray[:, :, 1])
    bleu = np.asarray(imageArray[:, :, 2])

    # parcourir pour crypté
    for x in range(hauteur):
        for y in range(0, largeur, 3):
            # part 1 rouge
            P1rouge, P2rouge, P3rouge = getP(key, rouge, x, y)
            # part 2 vert
            P1vert, P2vert, P3vert = getP(key, vert, x, y)
            # part 3 bleu
            P1bleu, P2bleu, P3bleu = getP(key, bleu, x, y)
            # part save changement
            imageArray[x, y] = (P1rouge, P1vert, P1bleu)
            imageArray[x, y + 1] = (P2rouge, P2vert, P2bleu)
            imageArray[x, y + 2] = (P3rouge, P3vert, P3bleu)

    # get image crypte
    image_crypte = img.fromarray(imageArray)
    image_crypte = image_crypte.convert("RGB")

    return image_crypte


def getP(key, color, x, y):
    C1 = color[x, y]
    C2 = color[x, y + 1]
    C3 = color[x, y + 2]
    P1 = (key[0] * C1 + key[1] * C2 + key[2] * C3) % modulo
    P2 = (key[3] * C1 + key[4] * C2 + key[5] * C3) % modulo
    P3 = (key[6] * C1 + key[7] * C2 + key[8] * C3) % modulo
    return P1, P2, P3


def dechiffrementImage(image_crypte, keyChiffrement):
    key = calcule_inverse_matrice_mod_n(keyChiffrement)
    return chiffrementImage(image_crypte, key)


print("lecture image")
image = img.open("img/chawki.png")
image.show()

print("generation cle")
key = generation_matrice_chiffrement()
print(key)

print("crypter image")
imageCrypte = chiffrementImage(image, key)

print(" show crypter image")
imageCrypte.show()

print("save image crypter")
imageCrypte.save("crypter.png")

print("decryptage image crypter")
imageDecrypte = dechiffrementImage(imageCrypte, key)

print("show decrypter image")
imageDecrypte.show()

print("save image decrypter")
imageDecrypte.save("decrypter.png")
