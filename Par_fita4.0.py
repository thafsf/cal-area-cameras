import cv2
import numpy as np

# Função para processar a imagem
def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray, (5, 5), 1.4)
    _, thresh = cv2.threshold(blurred_image, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(thresh, 50, 150)
    return edges, thresh

def overlay_contours_on_image(image, contour):
    # Copia a imagem original para sobrepor o contorno
    overlay = image.copy()

    # Desenha o contorno em vermelho (BGR: (0, 0, 255))
    cv2.drawContours(overlay, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

    # Transpor a imagem original e a imagem com contornos (50% de opacidade)
    final_image = cv2.addWeighted(overlay, 0.5, image, 0.5, 0)

    return final_image

# Função para calcular área, perímetro, média, mediana e maior largura da fita
def calculate_area_perimeter(edges, threshold_image, tape_width_meters=0.0176): # 0.0175 largura da fita de teste e 0.02 largura da fita na competição
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contour = max(contours, key=cv2.contourArea)
        area_pixels = cv2.contourArea(contour)
        perimeter_pixels = cv2.arcLength(contour, True)
        mask = np.zeros(edges.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        cv2.imshow('Imagem mask', mask)
        avg_tape_pixel_width = 9.0
#        tape_pixel_widths = []
#        for i in range(0, edges.shape[0], 10):
#            for j in range(0, edges.shape[1], 10):
#                if threshold_image[i, j] == 255:
#                    local_width = cv2.countNonZero(edges[i-5:i+5, j-5:j+5])
#                    if local_width > 0:
#                        tape_pixel_widths.append(local_width)
#        
#        if tape_pixel_widths:
#            avg_tape_pixel_width = np.mean(tape_pixel_widths)
#            med_tape_pixel_width = np.median(tape_pixel_widths)
#            max_tape_pixel_width = np.max(tape_pixel_widths)

        meters_per_pixel = tape_width_meters / avg_tape_pixel_width #tava antes avg_tape_pixel_width
        area_meters = area_pixels * (meters_per_pixel ** 2)
        perimeter_meters = perimeter_pixels * meters_per_pixel
        return area_meters, perimeter_meters, avg_tape_pixel_width

def Porcentagem_de_erro(area_calculada, perimetro_calculado):
    area_real = 0.16 #  metros quadrados
    perimetro_real = 2.23 # metros
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
        
        edges, thresh = process_image(image)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            contour = max(contours, key=cv2.contourArea)
        area, perimeter, avg_tape_pixel_width = calculate_area_perimeter(edges, thresh)
        erro_area, erro_per = Porcentagem_de_erro(area, perimeter)

        if area is not None and perimeter is not None:
            print(f"\nUtilizando a mediana da fita para cálculos:")
            print(f"\nÁrea: {area:.6f} metros quadrados")
            print(f"Perímetro: {perimeter:.6f} metros")
            print(f"Erro de área: {erro_area:.2f}%")
            print(f"Erro de perímetro: {erro_per:.2f}%\n")
        else:
            print("Nenhuma figura detectada.")
        
        final_image = overlay_contours_on_image(image, contour)

        # Exibir a imagem resultante
        cv2.imshow("Imagem com Contorno", final_image)
        cv2.imshow('Imagem Original', image)
        cv2.imshow('Imagem com Contornos', edges)
        cv2.waitKey(500)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()