import cv2
import numpy as np

# 1. Função para capturar imagem via Wi-Fi
#def capture_image(ip_address):
    # Captura o stream da câmera
  #  video_url = f"http://{ip_address}/video"  # Exemplo, pode ser RTSP ou outro
   # cap = cv2.VideoCapture(video_url)

   # ret, frame = cap.read()
   # if ret:
   #     return frame
   # else:
   #     print("Não foi possível capturar a imagem.")
   #     return None

# 2. Função para detectar bordas e fita preta (que forma os lados da figura)
def process_image(image):
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar threshold para isolar a fita preta (áreas escuras)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Detectar bordas usando Canny
    edges = cv2.Canny(thresh, 50, 150)

    return edges, thresh

def detect_black_edges(image):
    # Converter a imagem para tons de cinza
    gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar suavização para reduzir ruído
    blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    
    # Detectar as bordas usando Canny
    edges2 = cv2.Canny(blurred2, 50, 150)
    
    # Encontrar os contornos
    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

# 3. Função para calcular área e perímetro
def calculate_area_perimeter(edges, threshold_image, tape_width_meters=0.02):
    # Encontrar contornos na imagem
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Assumindo que o maior contorno é a figura
        contour = max(contours, key=cv2.contourArea)

        # Calcular área e perímetro em pixels
        area_pixels = cv2.contourArea(contour)
        perimeter_pixels = cv2.arcLength(contour, True)

        # Calcular a grossura da fita (em pixels)
        mask = np.zeros(edges.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # Encontrando a largura média da fita preta (as linhas que formam a figura)
        tape_pixel_widths = []

        for i in range(0, edges.shape[0], 10):  # Salta alguns pixels para melhorar a performance
            for j in range(0, edges.shape[1], 10):
                if threshold_image[i, j] == 255:  # Apenas considera áreas brancas (onde tem fita preta)
                    local_width = cv2.countNonZero(edges[i-5:i+5, j-5:j+5])
                    if local_width > 0:
                        tape_pixel_widths.append(local_width)

        if tape_pixel_widths:
            # Tira a média das larguras da fita em pixels
            avg_tape_pixel_width = np.mean(tape_pixel_widths)
            
            # Relação metros/pixel
            meters_per_pixel = tape_width_meters / avg_tape_pixel_width
            
            # Calcular área e perímetro em metros
            area_meters = area_pixels * (meters_per_pixel ** 2)
            perimeter_meters = perimeter_pixels * meters_per_pixel

            return area_meters, perimeter_meters, avg_tape_pixel_width
        else:
            print("Não foi possível calcular a largura da fita.")
            return None, None, None
    else:
        return None, None, None

# Função principal
def main():
    
    while True:# Captura a imagem da câmera
        camera_url = "http://192.168.1.6:4747/video"
        cap = cv2.VideoCapture(camera_url)
        
        while True:
        # Captura a imagem da câmera
            ret, image = cap.read()
            if not ret:
                print("Falha ao capturar frame")
                break    
            contours = detect_black_edges(image)
            largest_contour = max(contours, key=cv2.contourArea)
        # Processa a imagem para detectar a fita preta
            edges, thresh = process_image(image)

        # Calcula a área e o perímetro da figura
            area, perimeter, avg_tape_pixel_width = calculate_area_perimeter(edges, thresh)

            if area is not None and perimeter is not None:
                print(f"Área: {area:.4f} metros quadrados")
                print(f"Perímetro: {perimeter:.4f} metros")
                print(f"Largura média da fita em pixels: {avg_tape_pixel_width:.2f}")
            else:
                print("Nenhuma figura detectada.")

        # Desenha os contornos na imagem original
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
        
        # Mostra a imagem com os contornos
        cv2.imshow('Imagem com Contornos', image)
        
        # Mostra a imagem original
        cv2.imshow('Imagem Original', image)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
