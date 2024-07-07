import cv2 as cv
import mediapipe as mp
import numpy as np
import os

# Função para sobrepor uma imagem (sticker) em outra imagem (frame)
def overlay_image(frame, overlay, x, y, overlay_size=None):
    if overlay_size is not None:
        overlay = cv.resize(overlay, overlay_size, interpolation=cv.INTER_AREA)

    h, w = overlay.shape[:2]
    rows, cols = frame.shape[:2]

    # Garantir que o sticker não ultrapasse as bordas da imagem
    if x + w > cols:
        w = cols - x
    if y + h > rows:
        h = rows - y

    overlay = overlay[:h, :w]
    roi = frame[y:y+h, x:x+w]

    # Se a imagem do sticker tiver um canal alfa, separe-o
    if overlay.shape[2] == 4:
        overlay_rgb = overlay[:, :, :3]
        alpha_mask = overlay[:, :, 3]
    else:
        overlay_rgb = overlay
        alpha_mask = cv.cvtColor(overlay, cv.COLOR_BGR2GRAY)

    # Criar a máscara inversa
    alpha_inv = cv.bitwise_not(alpha_mask)

    # Converter a máscara para o tipo de dados uint8 se não for
    if alpha_inv.dtype != np.uint8:
        alpha_inv = alpha_inv.astype(np.uint8)

    # Aplicar a máscara e adicionar o sticker na região de interesse do frame
    overlayed_roi = cv.bitwise_and(roi, roi, mask=alpha_inv)
    frame[y:y+h, x:x+w] = cv.add(overlayed_roi, overlay_rgb)

# Inicializa a captura de vídeo da webcam
webcam = cv.VideoCapture(0)

# Inicializa o detector de rostos do MediaPipe
solucao_reconhecimento_rosto = mp.solutions.face_detection
reconhecer_rostos = solucao_reconhecimento_rosto.FaceDetection()
desenho = mp.solutions.drawing_utils

# Carrega a imagem do sticker
sticker_path = './stickers/eyeglasses.png'
print(f"Tentando carregar a imagem do sticker de '{sticker_path}'")
if not os.path.exists(sticker_path):
    print(f"Erro: O caminho '{sticker_path}' não existe. Verifique o caminho do arquivo.")
    exit()

sticker_img = cv.imread(sticker_path, cv.IMREAD_UNCHANGED)
if sticker_img is None:
    print(f"Erro: Não foi possível carregar a imagem '{sticker_path}'. Verifique se o arquivo é válido.")
    exit()

print("Imagem do sticker carregada com sucesso.")
print(f"Dimensões do sticker: {sticker_img.shape}")

# Fator de escala para ajustar o tamanho do sticker em relação ao tamanho dos olhos detectados
scale_factor = 0.8  # Altere este valor conforme necessário

while True:
    # Captura frame da webcam
    verificador, frame = webcam.read()

    if not verificador:
        break

    # Processa o frame para reconhecer rostos
    resultado = reconhecer_rostos.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

    # Se detectar rostos, desenha as detecções no frame e sobrepõe o sticker sobre os olhos
    if resultado.detections:
        for rosto in resultado.detections:
            bboxC = rosto.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            # Calcula as coordenadas e tamanho dos olhos
            x_eye = int(bboxC.xmin * iw)
            y_eye = int(bboxC.ymin * ih)
            w_eye = int(bboxC.width * iw) 
            h_eye = int(bboxC.height * ih) -50 

            # Define o tamanho do sticker com base no tamanho dos olhos
            sticker_size = (int(w_eye * scale_factor), int(h_eye * scale_factor))
            print(f"Sobrepondo sticker nos olhos com tamanho: ({sticker_size[0]}, {sticker_size[1]})")

            # Calcula a posição para o sticker estar centralizado nos olhos
            x_sticker = x_eye + (w_eye // 2) - (sticker_size[0] // 2)
            y_sticker = y_eye + (h_eye // 2) - (sticker_size[1] // 2)

            overlay_image(frame, sticker_img, x_sticker, y_sticker, sticker_size)

    # Exibe o frame com as detecções e os stickers
    cv.imshow("Rostos em Webcam com Stickers", frame)

    # Interrompe o loop se a tecla ESC (27) for pressionada
    if cv.waitKey(5) == 27:
        cv.imwrite('Mask com mediapipe.png', frame)
        break

# Libera a webcam e fecha todas as janelas
webcam.release()
cv.destroyAllWindows()
