import cv2
import numpy as np

retangulo = {'x': 0, 'y': 0, 'width': 0, 'height': 0}

imagemoriginal = cv2.imread("Figura_teste2.jpeg")

def manual_calculation(event, x, y, flags, param):
    global retangulo
    if event == cv2.EVENT_LBUTTONDOWN:
        retangulo['x'] = x
        retangulo['y'] = y
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            retangulo['width'] = x - retangulo['x']
            retangulo['height'] = y - retangulo['y']
    #print(f"Posição do mouse: ({x}, {y})")

cv2.namedWindow("Imagem", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Imagem", manual_calculation)

tecla = ''
while tecla != ord('t'):
    # Faz uma cópia da imagem original para preservá-la
    imagemclone = imagemoriginal.copy()

    # Desenha o retângulo
    cv2.rectangle(imagemclone, (retangulo['x'], retangulo['y']),
                  (retangulo['x'] + retangulo['width'], retangulo['y'] + retangulo['height']),
                  (255, 0, 0), 2)
    print(f"Retângulo: Largura({retangulo['width']}), Altura({retangulo['height']})")
    # Mostra a imagem com o retângulo desenhado
    cv2.imshow("Imagem", imagemclone)

    # Aguarda por 100ms para capturar a próxima tecla
    tecla = cv2.waitKey(100) & 0xFF

# Fecha todas as janelas
cv2.destroyAllWindows()