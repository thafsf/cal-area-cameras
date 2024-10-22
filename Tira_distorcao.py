import cv2
import numpy as np

# Função para corrigir distorção em cada quadro
def undistort_frame(frame, camera_matrix, dist_coeffs):
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))

    # Corrigir distorção no frame
    undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    # Recortar a imagem se necessário (ROI - região de interesse)
    x, y, w, h = roi
    undistorted_frame = undistorted_frame[y:y+h, x:x+w]

    return undistorted_frame

# Função principal para capturar vídeo e aplicar correção de distorção
def main(camera_matrix, dist_coeffs):
    cap = cv2.VideoCapture('Video_de_teste_3.mp4')

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            break
            

        # Corrigir distorção no quadro
        undistorted_frame = undistort_frame(frame, camera_matrix, dist_coeffs)

        # Exibir o vídeo original e corrigido lado a lado
        combined_frame = np.hstack((frame, undistorted_frame))
        cv2.imshow("Original vs Corrigido", combined_frame)
        cv2.waitkey(500)
        # Pressionar 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar a captura e fechar as janelas
    cap.release()
    cv2.destroyAllWindows()

# Definir parâmetros intrínsecos da câmera (após calibração)
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])  # Substitua pelos valores calibrados
dist_coeffs = np.array([-0.2, 0.1, 0, 0, 0])  # Substitua pelos coeficientes calibrados


