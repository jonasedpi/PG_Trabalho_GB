import cv2 as cv
import numpy as np

def grayScale(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return cv.cvtColor(gray_img, cv.COLOR_GRAY2BGR)

def blur(img):
    return cv.blur(img, (5, 5))

def negativo(img):
    return cv.bitwise_not(img)

def bilateral(img):
    return cv.bilateralFilter(img, 15, 75, 75)

def denoised(img):
    return cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

def realce_contraste(img):
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    clahe_image = clahe.apply(gray_image)
    return cv.cvtColor(clahe_image, cv.COLOR_GRAY2BGR)

def sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_filter = cv.transform(img, kernel)
    sepia_filter = np.clip(sepia_filter, 0, 255)
    return sepia_filter.astype(np.uint8)

def affine(img):
    rows, cols, ch = img.shape
    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
    M = cv.getAffineTransform(pts1, pts2)
    return cv.warpAffine(img, M, (cols, rows))

def perspective(img):
    pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
    pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    return cv.warpPerspective(img, M, (300, 300))

def saturacao(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    s = cv.add(s, 30)
    enhanced_hsv = cv.merge([h, s, v])
    return cv.cvtColor(enhanced_hsv, cv.COLOR_HSV2BGR)

def equalizacao(img):
    img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])
    return cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)

def canny(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray_img, 50, 100)
    return cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

def escolhendo_efeito(img, string):
    if string == 'G' or string == 'g':
        return grayScale(img)
    if string == 'B' or string == 'b':
        return blur(img)
    if string == 'N' or string == 'n':
        return negativo(img)
    if string == 'L' or string == 'l':
        return bilateral(img)
    if string == 'D' or string == 'd':
        return denoised(img)
    if string == 'C' or string == 'c':
        return realce_contraste(img)
    if string == 'S' or string == 's':
        return sepia(img)
    if string == 'A' or string == 'a':
        return affine(img)
    if string == 'P' or string == 'p':
        return perspective(img)
    if string == 'E' or string == 'e':
        return equalizacao(img)
    if string == 'T' or string == 't':
        return canny(img)
    if string == 'Ç' or string == 'ç':
        return saturacao(img)
''
# Exemplo de uso:
# img = cv.imread('Foto_C.png')
# resultado = escolhendo_efeito(img, 'G')
# cv.imshow("Resultado", resultado)
# cv.waitKey(0)
# cv.destroyAllWindows()
