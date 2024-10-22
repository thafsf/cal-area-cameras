import cv2
#import numpy as np
#import requests

# Função para capturar a imagem via Wi-Fi
#def capture_image_from_wifi(camera_url):
    # Baixa a imagem da câmera (URL fornecida pela API da câmera)
    #response = requests.get(camera_url)
    #image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    #img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    #return img

def detect_black_edges(img):
    # Converter a imagem para tons de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar suavização para reduzir ruído
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detectar as bordas usando Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Encontrar os contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def calculate_area_perimeter(contours, distance_from_camera):
    for contour in contours:
        # Calcular a área
        area = cv2.contourArea(contour)
        # Calcular o perímetro
        perimeter = cv2.arcLength(contour, True)

        # Ajustar o cálculo com base na distância fornecida
        # O fator de escala depende da lente da câmera e da geometria
        scale_factor = 1 / distance_from_camera  # Ajuste isso conforme necessário
        scaled_area = area * scale_factor
        scaled_perimeter = perimeter * scale_factor
        
        return scaled_area, scaled_perimeter
    return None, None

def main():
    camera_url = "http://192.168.1.6:4747/video"
    cap = cv2.VideoCapture(camera_url)
    distance_from_camera = 0.58 # Distância da câmera ao objeto em metros
    while True:
        # Captura a imagem da câmera
        ret, img = cap.read()
        if not ret:
            print("Falha ao capturar frame")
            break
        img2 = img.copy()
        # Detecta os contornos da figura
        contours = detect_black_edges(img)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Se contornos foram encontrados, calcula a área e o perímetro
        if contours:
            area, perimeter = calculate_area_perimeter(contours, distance_from_camera)
            
            if area and perimeter:
                print(f"Área ajustada: {area:.2f} unidades quadradas")
                print(f"Perímetro ajustado: {perimeter:.2f} unidades")
            else:
                print("Nenhuma figura com arestas pretas foi detectada.")
        else:
            print("Nenhuma figura detectada.")

        # Exibir a imagem original e os contornos encontrados
        cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 2)
        cv2.imshow('Imagem com Contornos', img)
        cv2.imshow('Imagem Original', img)
        
        # Aguardando um pequeno intervalo de tempo para o próximo frame (30 ms)
        # Pressione 'q' para sair do loop
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
