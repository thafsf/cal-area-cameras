import cv2
import numpy as np

# Função para processar a imagem
def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
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
        print(f"Perímetro em pixels: {perimeter_pixels}")
        mask = np.zeros(edges.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        cv2.imshow('Imagem mask', mask)
        
        tape_pixel_widths = []
        for i in range(0, edges.shape[0], 10):
            for j in range(0, edges.shape[1], 10):
                if threshold_image[i, j] == 255:
                    local_width = cv2.countNonZero(edges[i-5:i+5, j-5:j+5])
                    if local_width > 0:
                        tape_pixel_widths.append(local_width)
        
        if tape_pixel_widths:
            avg_tape_pixel_width = np.mean(tape_pixel_widths)
            med_tape_pixel_width = np.median(tape_pixel_widths)
            max_tape_pixel_width = np.max(tape_pixel_widths)

            meters_per_pixel = tape_width_meters / med_tape_pixel_width #tava antes avg_tape_pixel_width
            area_meters = area_pixels * (meters_per_pixel ** 2)
            perimeter_meters = perimeter_pixels * meters_per_pixel

            return area_meters, perimeter_meters, avg_tape_pixel_width, med_tape_pixel_width, max_tape_pixel_width
        else:
            print("Não foi possível calcular a largura da fita.")
            return None, None, None, None, None
    else:
        return None, None, None, None, None

def Porcentagem_de_erro(area_calculada, perimetro_calculado):
    area_real = 0.008925 #  metros quadrados
    perimetro_real = 0.38 # metros
    erro_area = ((area_real - area_calculada) / area_real) * 100
    erro_per = ((perimetro_real - perimetro_calculado) / perimetro_real) * 100
    
    return erro_area, erro_per

# Função principal
def main():
    image = cv2.imread("Figura_teste2.jpeg")
    
    if image is None:
        print("Falha ao carregar a imagem")
        return
    
    edges, thresh = process_image(image)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        contour = max(contours, key=cv2.contourArea)
        area, perimeter, avg_tape_pixel_width, med_tape_pixel_width, max_tape_pixel_width = calculate_area_perimeter(edges, thresh)
        erro_area, erro_per = Porcentagem_de_erro(area, perimeter)

        if area is not None and perimeter is not None:
            print(f"\nUtilizando a mediana da fita para cálculos:")
            print(f"\nÁrea: {area:.6f} metros quadrados")
            print(f"Perímetro: {perimeter:.6f} metros")
            print(f"Largura média da fita em pixels: {avg_tape_pixel_width:.2f}")
            print(f"Largura mediana da fita em pixels: {med_tape_pixel_width:.2f}")
            print(f"Maior largura da fita em pixels: {max_tape_pixel_width:.2f}")
            print(f"Erro de área: {erro_area:.2f}%")
            print(f"Erro de perímetro: {erro_per:.2f}%\n")
        else:
            print("Nenhuma figura detectada.")
        
        final_image = overlay_contours_on_image(image, contour)

        # Exibir a imagem resultante
        cv2.imshow("Imagem com Contorno", final_image)
        cv2.imshow('Imagem Original', image)
        cv2.imshow('Imagem com Contornos', edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
