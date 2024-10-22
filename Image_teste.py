import cv2

def detect_black_edges(img2):
    # Converter a imagem para tons de cinza
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    #eroded = cv2.erode(gray, kernel, iterations=1)
    #dilated = cv2.dilate(eroded, kernel, iterations=1)
    #while True:
        #cv2.imshow('Imagem eroded', eroded)
        #cv2.imshow('Imagem dilated', dilated)
        #cv2.imshow('Imagem gray', gray)
        #if cv2.waitKey(30) & 0xFF == ord('q'):
            #break
    # Aplicar suavização para reduzir ruído
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) #blurred = cv2.GaussianBlur(gray, (7, 7), 0) pega a área de dentro da figura
    
    # Detectar as bordas usando Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Encontrar os contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def calculate_area_perimeter(contour, distance_from_camera):
    # Calcular a área
    area = cv2.contourArea(contour)
    # Calcular o perímetro
    perimeter = cv2.arcLength(contour, True)

    # Ajustar o cálculo com base na distância fornecida
    # O fator de escala depende da lente da câmera e da geometria
    #scale_factor = 1 / distance_from_camera  # Ajuste isso conforme necessário
    scaled_area = area #* scale_factor
    scaled_perimeter = perimeter #* scale_factor
    
    return scaled_area, scaled_perimeter

def main():
    distance_from_camera = 0.53 # Distância da câmera ao objeto em metros
    img = cv2.imread('Figura_teste2.jpeg', cv2.IMREAD_COLOR)     
    img2 = img.copy()
    contours = detect_black_edges(img2)
        
    # Se contornos foram encontrados, calcula a área e o perímetro do maior contorno
    if contours:
        # Encontrar o contorno com a maior área
        largest_contour = max(contours, key=cv2.contourArea)
        area, perimeter = calculate_area_perimeter(largest_contour, distance_from_camera)
            
        if area and perimeter:
            print(f"Área ajustada: {area:.2f} metros quadrados")
            print(f"Perímetro ajustado: {perimeter:.2f} metros")
        else:
            print("Nenhuma figura com arestas pretas foi detectada.")
        # Exibir a imagem original e o contorno encontrado
        cv2.drawContours(img2, [largest_contour], -1, (0, 255, 0), 2)
    
    while True:
        cv2.imshow('Imagem Original', img)
        cv2.imshow('Imagem com Contornos', img2)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()