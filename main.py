import os
import cv2 as cv
import sys

from controleWebcam import tirarFoto
import filtro
import sticker

def listar_imagens(diretorio):
    arquivos = os.listdir(diretorio)
    return [arquivo for arquivo in arquivos if arquivo.endswith(('.jpg', '.png'))]

def main():
    menu = input('No que deseja colocar efeitos ou/e stickers: Fotos = F CAM = C ')
    path_dir = "./imagens/"
    path_dir_sticker = './stickers/'
    editando = True
    img = ''
    img_editando = ''

    if menu.lower() == 'f':
        imagens = listar_imagens(path_dir)
        print(imagens)
        foto_escolhida = input("Digite o index da foto escolhida:")
        img = cv.imread(os.path.join(path_dir, imagens[int(foto_escolhida)]))
    elif menu.lower() == 'c':
        tirarFoto()
        img = cv.imread('Foto_C.png')

    img_editando = img.copy()

    while editando:
        cv.imshow("Editando a imagem", img_editando)
        cv.waitKey(1)

        print('G = GrayScale \n B = blur \n N = Negativo \n L = bilateral \n'
              + "D = Denoise \n C = Contraste \n S = Sepia \n A = affine \n "
              + 'P = persperctive \n ç = saturação\n E = equilazação \n'
              + 'T = Canny \n R = reset \n terminar a edição = Y')
        
        efeito = input('Digite qual efeito quer colocar na sua foto ?')
        
        if efeito.lower() == 'y':
            editando = False
        elif efeito.lower() == 'r':
            img_editando = img.copy()
        else:
            img_editando = filtro.escolhendo_efeito(img_editando, efeito)
        
        cv.imwrite('Foto_edi.png', img_editando)
        cv.destroyAllWindows()

    arquivos_sticker = listar_imagens(path_dir_sticker)
    print(arquivos_sticker)
    sticker_escolhido = input("Digite o index da sticker escolhida:")

    sticker.adicionar_sticker_com_mouse('Foto_edi.png', os.path.join(path_dir_sticker, arquivos_sticker[int(sticker_escolhido)]))

    img_editando = cv.imread('foto_finalizada.png')
    cv.imshow("Foto finalizada", img_editando)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
