import os
import cv2 as cv
import sys

from controleWebcam import tirarFoto
import filtro
import sticker

menu = input('No que deseja colocar efeitos ou/e stickers: Fotos = F CAM = C ')
path_dir = "./imagens/"
path_dir_sticker = './stickers/'
editando = True
img = ''
img_editando = ''

if menu == 'F' or menu == 'f':
   # Liste todos os arquivos no diretório
   arquivos = os.listdir(path_dir)

   # Filtre apenas os arquivos de imagem (por exemplo, com extensão .jpg ou .png)
   imagens = [arquivo for arquivo in arquivos if arquivo.endswith(('.jpg', '.png'))]

   # Retorne a lista de imagens ou apenas um nome de arquivo
   print(imagens)

   foto_escolhida = input("Digite o index da foto escolhida:")

   img = cv.imread('./imagens/'+ imagens[(int)(foto_escolhida)])
   img_editando = img.copy()
   
if menu == 'C' or menu == 'c':

   tirarFoto()
   img = cv.imread('Foto_C.png')
   img_editando = img.copy()
   

while editando:

   cv.imshow("Editando a imagem", img_editando)

   print('G = GrayScale \n B = blur \n N = Negativo \n L = bilateral \n'
               + "D = Denoise \n C = Contraste \n S = Sepia \n A = affine \n "
               + 'P = persperctive \n ç = saturação\n E = equilazação \n'
               +'T = Canny \n R = reset \n terminar a edição = Y'
               )
   efeito = input('Digite qual efeito quer colocar na sua foto ?')
      
   if efeito == 'y' or efeito == 'Y':
         editando = False
   elif efeito == 'r' or efeito == 'R':
         img_editando = img.copy()
   else:
         img_editando = filtro.escolhendo_efeito(img_editando, efeito)
   cv.imwrite('Foto_edi.png', img_editando)


cv.imshow("Editando a imagem", img_editando)
# Liste todos os arquivos no diretório
arquivos = os.listdir(path_dir_sticker)

   # Filtre apenas os arquivos de imagem (por exemplo, com extensão .jpg ou .png)
stic = [arquivo for arquivo in arquivos if arquivo.endswith(('.jpg', '.png'))]

   # Retorne a lista de imagens ou apenas um nome de arquivo

print(stic)

sticker_escolhido = input("Digite o index da sticker escolhida:")

sticker.adicionar_sticker_com_mouse('Foto_edi.png', './stickers/' + stic[(int)(sticker_escolhido)])

img_editando = cv.imread('foto_finalizada.png')
cv.imshow("Foto finalizado",img_editando)
cv.waitKey(0)
cv.destroyAllWindows
