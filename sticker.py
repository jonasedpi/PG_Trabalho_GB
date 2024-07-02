import cv2 as cv
import numpy as np

def adicionar_sticker_com_mouse(imagem_path, sticker_path):
    global img_editando, sticker, colocando

    # Carregar a imagem e o sticker
    img_editando = cv.imread(imagem_path, cv.IMREAD_UNCHANGED)
    sticker = cv.imread(sticker_path, cv.IMREAD_UNCHANGED)

    if img_editando is None or sticker is None:
        print("Erro ao carregar a imagem ou o sticker.")
        return

    colocando = True

    # Mostrar a imagem e configurar o callback do mouse
    cv.imshow("Editando a imagem", img_editando)
    cv.setMouseCallback("Editando a imagem", colocar_sticker)

    while True:
        cv.imshow("Editando a imagem", img_editando)
        tecla = cv.waitKey(1) & 0xFF
        if tecla == ord('q'):  # Pressione 'q' para sair
            cv.imwrite('foto_finalizada.png', img_editando)  # Salvar a imagem
            break

    cv.destroyAllWindows()

def colocar_sticker(event, x, y, flags, param):
    global img_editando, sticker

    if event == cv.EVENT_LBUTTONDOWN:
        posicao = (x, y)
        adicionar_sticker(img_editando, sticker, posicao)

def adicionar_sticker(imagem, sticker, posicao):
    x_offset, y_offset = posicao
    y1, y2 = y_offset, y_offset + sticker.shape[0]
    x1, x2 = x_offset, x_offset + sticker.shape[1]

    if y2 > imagem.shape[0]:
        y2 = imagem.shape[0]
        sticker = sticker[:y2 - y1, :]
    if x2 > imagem.shape[1]:
        x2 = imagem.shape[1]
        sticker = sticker[:, :x2 - x1]

    alpha_s = sticker[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        imagem[y1:y2, x1:x2, c] = (alpha_s * sticker[:, :, c] +
                                   alpha_l * imagem[y1:y2, x1:x2, c])