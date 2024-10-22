import cv2
import numpy as np

retangulo = {'x': 0, 'y': 0, 'width': 0, 'height': 0}

# Abre o vídeo
video = cv2.VideoCapture("Video_de_teste_3.mp4")

def manual_calculation(event, x, y, flags, param):
    global retangulo
    if event == cv2.EVENT_LBUTTONDOWN:
        retangulo['x'] = x
        retangulo['y'] = y
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            retangulo['width'] = x - retangulo['x']
            retangulo['height'] = y - retangulo['y']

cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Video", manual_calculation)

while True:
    ret, frame = video.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray, (5, 5), 1.4)
    _, thresh = cv2.threshold(blurred_image, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(thresh, 50, 150)
    # Desenha o retângulo
    cv2.rectangle(frame, (retangulo['x'], retangulo['y']),
                  (retangulo['x'] + retangulo['width'], retangulo['y'] + retangulo['height']),
                  (255, 0, 0), 2)
    print(f"Retângulo: Largura({retangulo['width']}), Altura({retangulo['height']})")
    
    # Mostra o frame com o retângulo desenhado
    cv2.imshow("Video", edges)
    
    # Aguarda até que a tecla 'Q' seja pressionada
    tecla = cv2.waitKey(0) & 0xFF
    if tecla == ord('q'):
        continue
    elif tecla == ord('t'):
        break

# Libera o vídeo e fecha todas as janelas
video.release()
cv2.destroyAllWindows()