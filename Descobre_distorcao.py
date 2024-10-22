import cv2
import numpy as np

# Definir o tamanho do padrão de xadrez (número de cantos interiores)
checkerboard_size = (9, 6)
# Preparar pontos 3D no espaço real (0,0,0), (1,0,0), (2,0,0), ...
objp = np.zeros((np.prod(checkerboard_size), 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)

# Vetores para armazenar pontos no mundo real e os pontos detectados na imagem
objpoints = []  # Pontos 3D
imgpoints = []  # Pontos 2D

# Capturar várias imagens do tabuleiro de xadrez
for i in range(10):  # Substitua pela quantidade de imagens que você capturar
    img = cv2.imread(f'chessboard_image_{i}.jpg')  # Substitua pelo caminho das suas imagens
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Encontrar os cantos do tabuleiro de xadrez
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Desenhar os cantos detectados
        cv2.drawChessboardCorners(img, checkerboard_size, corners, ret)
        cv2.imshow('Padrão Xadrez', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Calibrar a câmera
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Matriz da Câmera:")
print(camera_matrix)

print("Coeficientes de Distorção:")
print(dist_coeffs)
