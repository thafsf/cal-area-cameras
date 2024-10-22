import cv2
import numpy as np

# Função para processar a imagem
def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray, (5, 5), 1.4)
    _, thresh = cv2.threshold(blurred_image, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(thresh, 50, 150)
    return edges, thresh

# Função para detectar bordas pretas
def detect_black_edges(image):
    gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    edges2 = cv2.Canny(blurred2, 50, 150)
    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def identify_shape_and_calculate_area(contour, meters_per_pixel):
    # Aproxima o contorno para simplificar a forma
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Contar o número de vértices da figura aproximada
    vertices = len(approx)
    shape_name = "Desconhecida"

    # Calcular a área do contorno em pixels
    area_pixels = cv2.contourArea(contour)

    # Determinar a forma com base no número de vértices
    if vertices == 3:
        shape_name = "Triângulo"
        area_meters = area_pixels * (meters_per_pixel ** 2)
    elif vertices == 4:
        # Para quadrado ou retângulo, verificar proporção dos lados
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            shape_name = "Quadrado"
        else:
            shape_name = "Retângulo"
        area_meters = area_pixels * (meters_per_pixel ** 2)
    elif vertices > 4:
        # Consideramos figuras com mais de 4 lados como círculos ou polígonos regulares
        shape_name = "Círculo" if vertices > 8 else "Polígono"
        area_meters = area_pixels * (meters_per_pixel ** 2)
    else:
        area_meters = None

    return shape_name, area_meters

# Função para calcular área e perímetro
def calculate_area_perimeter(edges, threshold_image, tape_width_meters=0.02): # 0.0175 largura da fita de teste e 0.02 largura da fita na competição
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        contour = max(contours, key=cv2.contourArea)
        area_pixels = cv2.contourArea(contour)
        perimeter_pixels = cv2.arcLength(contour, True)
        mask = np.zeros(edges.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        tape_pixel_widths = []
        for i in range(0, edges.shape[0], 10):
            for j in range(0, edges.shape[1], 10):
                if threshold_image[i, j] == 255:
                    local_width = cv2.countNonZero(edges[i-5:i+5, j-5:j+5])
                    if local_width > 0:
                        tape_pixel_widths.append(local_width)
        if tape_pixel_widths:
            avg_tape_pixel_width = np.mean(tape_pixel_widths)
            meters_per_pixel = tape_width_meters / avg_tape_pixel_width
            area_meters = area_pixels * (meters_per_pixel ** 2)
            perimeter_meters = perimeter_pixels * meters_per_pixel
            print(f"avg_tape_pixel_width: {avg_tape_pixel_width}")
            print(f"area_meters: {area_meters}")
            return area_meters, perimeter_meters, avg_tape_pixel_width
        else:
            print("Não foi possível calcular a largura da fita.")
            return None, None, None
    else:
        return None, None, None

def Porcentagem_de_erro(area_calculada, perimetro_calculado):
    area_real = 0.16
    perimetro_real = 2.10
    erro_area = ((area_real - area_calculada) / area_real) * 100
    erro_per = ((perimetro_real - perimetro_calculado) / perimetro_real) * 100
    
    return erro_area, erro_per

# Função principal
def main():
    #camera_url = "http://192.168.1.6:4747/video"
    #cap = cv2.VideoCapture(camera_url)
    cap = cv2.VideoCapture("Video_de_teste_3.mp4")
    
    while True:
        ret, image = cap.read()
        if not ret:
            print("Falha ao capturar frame")
            break
        
        contours = detect_black_edges(image)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
        else:
            largest_contour = None
        
        edges, thresh = process_image(image)
        area, perimeter, avg_tape_pixel_width = calculate_area_perimeter(edges, thresh)
        Porcentagem_de_erro(area, perimeter)
        if area is not None and perimeter is not None:
            print(f"\nÁrea: {area:.6f} metros quadrados")
            print(f"Perímetro: {perimeter:.6f} metros")
            print(f"Largura média da fita em pixels: {avg_tape_pixel_width:.2f}")
            print(f"Erro de área: {Porcentagem_de_erro(area, perimeter)[0]:.2f}%")
            print(f"Erro de perímetro: {Porcentagem_de_erro(area, perimeter)[1]:.2f}%\n")
        else:
            print("Nenhuma figura detectada.")

        if largest_contour is not None:
            cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
        
        cv2.imshow('Imagem Original', image)
        cv2.imshow('Imagem com edges', edges)
        cv2.imshow('Imagem com thresh', thresh)
        cv2.waitKey(1000)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()