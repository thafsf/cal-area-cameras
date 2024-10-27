  pip install opencv-python numpy requests

Figura_teste - câmera a 0.58m de distância da figura, não perpendicular a ela

Figura_teste2 - câmera a 0.53m de distância da figura e está perpendicular a ela

  Parte de fora da fita - largura 0.105m e altura 0.085m, área 0.008925m² e perímetro 0.38m

  Parte de dentro da figura - largura 0.07m e altura 0.05m, área 0.0035m² e perímetro 0.22m

  0.0176m largura da fita de teste e 0.02m largura da fita na competição


Entregando o resultados parecidos e próximos do esperado:

Par_fitaAtual - Filtra as figuras baseada na largura da fita, em pixels, dada(necessita usar o manual_cal_video) 
Par_fitaAtualCom2.0 - Filtra as figuras baseada na largura da fita, em pixels, dada(necessita usar o manual_cal_video) e não há cálculo de erro de área ou perímetro
Par_fitaAtualCom - Não há cálculo de erro de área ou perímetro

Utilize o manual_cal_video.py para calcular a largura da fita em pixels do Par_fitaAtual.py

manual_cal_video.py: Pressione a tecla Q para pular os frames, clique e arraste o mouse na tela para gerar um retângulo no frame escolhido, depois aperte Q para que o retâgulo apareça

