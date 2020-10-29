# Esteganografia-bmp
Resumo

	O programa foi feito com intenção de integrar uma mensagem em uma imagem, substituindo bits de cada pixel pelos bits da mensagem, e fazer o processo inverso, extraindo uma mensagem de uma imagem. O programa consiste em 2 funções principais e 3 funções de apoio e utiliza a biblioteca PILLOW para acessar a classe “Image” e poder ler e alterar seus atributos.

Encriptação

	Cada pixel de uma imagem bmp é formado por 3 valores RGB que variam entre 0 e 255 (0000000 e 1111111 em binário). O processo de encriptação transcreve a mensagem desejada para binário e armazena cada um de seus bits nos pixels da imagem alterando o bit menos importante de cada valor RGB (o último bit), tal alteração é tão pequena que é raramente perceptível pelo olho humano nú. Pensando no processo de decriptação é adicionado anteriormente a mensagem um “cabeçalho” em binário composto pela extensão da mensagem e um separador pré-definido.
Decriptação

	São lidos os bits menos importantes de cada valor RGB dos pixels de uma imagem e formados caracteres de acordo com seus respectivos valores ASCII até ser encontrado o caractere separador. O número formado pelos caracteres anteriores ao caractere separador indica o tamanho da mensagem e permite-nos saber até que valor RGB em que pixel devemos ler para formar a mensagem completa. Os bits são lidos traduzidos do começo ao fim e é formada a mensagem. 
