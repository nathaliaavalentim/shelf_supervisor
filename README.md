
O Operador Sobel é comumente usado para detecção de bordas em imagens. 
No processo de convolução, o operador aplica um kernel à imagem, multiplicando os valores dos pixels da imagem pelos valores correspondentes do kernel e somando os resultados para obter o valor do pixel resultante. 

Defini os kernels Sobel para detecção de bordas na direção horizontal e vertical, e apliquei esses kernels à imagem original para calcular as derivadas em relação aos eixo horizontal e ao eixo vertical.

A relação entre o Operador Sobel e as derivadas é que os kernels Sobel aplicam operações de convolução na imagem. Assim ao aplicar os kernels Sobel, calcula-se as aproximações das derivadas horizontais e verticais da imagem em relação às coordenadas x e y.

O operador Sobel será 0 em regiões da imagem onde há indicativos de que não há bordas. E, ao contrário, terá o valor alto onde houver mudança significativa de intensidade de cor em um direção específica (vertical ou horizontal), indicando assim que há bordas.

Em relação a destacar as bordas, adicionei a função apply_threshold para aplicar um limiar na magnitude das bordas calculadas a partir das bordas horizontais e verticais (representadas por border_x e border_y). Usei threshold_value = 100 pra ajustar o valor do limiar para destacar as bordas desejadas na imagem final, mas o valor pode ser alterado.

No código, optei por usar a lib Pillow do Python, por ser comumente usada para trabalhar com imagens e é relativamente simples de usar. Já as libs numpy e matplotlib, para conseguir usar a função arctan2 no desenho de mapas de cores e fazer a visualização. 

Para filtrar os ângulos e apenas desenhar os ângulos entre cerca de 45 graus, apliquei uma máscara aos ângulos antes de exibir no mapa de cores, onde np.where é usada para aplicar essa máscara, substituindo os ângulos fora desse intervalo por np.nan, e então esses angulos são ignorados ao exibir o mapa de cores.

O ângulo de 45 graus não cobre todas as diagonais com inclinação positiva porque a definição padrão de ângulos em relação aos eixos x e y não abrange todas as possíveis inclinações de linhas diagonais. Por isso, fiz um ajuste na máscara com o objetivo de incluir todas as diagonais com inclinação positiva (ângulos de 0 a 90 graus).

Já para encontrar cantos que formem um ângulo de 90 graus com uma linha vertical à direita e uma linha horizontal no topo, encontrei mais dificuldades, apliquei uma máscara específica nos ângulos para identificar essas características.  Usei a função find_corners que verifica se um pixel destacado representa um canto com ângulo de 90 graus e é uma função que pode trabalhar com objetos PIL.Image (lib Pillow). 

Para filtrar a imagem para que não detectemos bordas atípicas de pixels ruidosos, adicionei a função cv2.GaussianBlur para aplicar o filtro Gaussiano à imagem em escala de cinza antes de calcular os gradientes.

Para as linhas verticais, utilizei a função cv2.HoughLinesP para detecção.
