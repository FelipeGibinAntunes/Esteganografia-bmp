from PIL import Image

# variáveis
separador = "@"
imagemBase = ""
imagemNova = ""
mensagem = ""
inp = ""

# conversor de caractéres alfanuméricos para valores binários
def CharParaBin(s):
    out = ""
    bits = ""
    for c in s:
        bits = bin(ord(c))[2::]
        while len(bits) < 7:
            bits = "0" + bits
        out = out + bits
    return out

# conversor de valores binários para caractéres alfanuméricos
def BinParaChar(s):
    out = ""
    bits = ""
    for c in s:
        if len(bits) < 7:
            bits = bits + c
        if len(bits) == 7:
            out = out + chr(int(bits,2))
            bits = ""
    return out

# criador do cabeçalho da mensagem (composto pelo número de caractéres da mensagem seguido do separador - é usado na decriptação)
def CabecalhoMensagem(msg, sep):
    out = ""
    msgb = CharParaBin(msg)
    qnt = str(len(msgb))
    out = CharParaBin(qnt) + CharParaBin(sep)
    return out

def Encriptador(msg, img, newimg, sep):
    # variáveis para controlar o pixel e o valor RGB alterados em cada instância
    pxatual = 0
    pyatual = 0
    index = 0
    comprimento = img.size[1]

    # a mensagem completa em bits incluindo o cabeçalho
    bits = CabecalhoMensagem(msg, sep) + CharParaBin(msg)
    for b in bits:
        # converter o valor RGB atual em binário e armazená-lo em "temp"
        temp = bin(img.load()[pxatual, pyatual][index])[2::]
        # setar o ultimo bit de "temp" para "b" (o bit da mensagem atual)
        temp = temp[:-1] + b
        # converter "temp" para decimal e alterar o valor RGB atual
        if index == 0:
            img.load()[pxatual, pyatual] = (int(temp,2),img.load()[pxatual,pyatual][1],img.load()[pxatual,pyatual][2])
        if index == 1:
            img.load()[pxatual, pyatual] = (img.load()[pxatual,pyatual][0],int(temp,2),img.load()[pxatual,pyatual][2])
        if index == 2:
            img.load()[pxatual, pyatual] = (img.load()[pxatual,pyatual][0],img.load()[pxatual,pyatual][1],int(temp,2))      
        # gerenciar os índices
        index = index + 1
        if index == 3:
            index = 0
            pxatual = pxatual + 1
        if pxatual == comprimento:
            pxatual = 0
            pyatual = pyatual + 1
    # salvar as mudanças feitas em uma nova imagem
    img.save(newimg)
    print("Encriptado com sucesso!")

def Decriptador(img, sep):
    # variáveis para controlar o pixel e o valor RGB lidos em cada instância
    pxatual = 0
    pyatual = 0
    index = 0
    comprimento = img.size[1]
    # variáveis para gerenciar o texto decriptado
    atual = ""
    cabecalho = ""
    out = ""

    while True:
        # adiciona a "atual" o último bit do valor RGB lido
        l = len(bin(img.load()[pxatual, pyatual][index])[2::])
        atual = atual + bin(img.load()[pxatual, pyatual][index])[1+l::]
        # gerencia os índices
        index = index + 1
        if index == 3:
            index = 0
            pxatual = pxatual + 1
        if pxatual == comprimento:
            pxatual = 0
            pyatual = pyatual + 1
        # converte o valor de "atual" para um caractére alfanumérico e checa se é o separador; caso não seja, o adiciona no cabeçalho; o processo termina ao encontrar o separador
        if len(atual) == 7:
            if BinParaChar(atual) == sep:
                break
            cabecalho = cabecalho + BinParaChar(atual)
            atual = ""
    # salva os bits indicados pelo cabeçalho      
    for _ in range(0, int(cabecalho)):
        l = len(bin(img.load()[pxatual, pyatual][index])[2::])
        out = out + bin(img.load()[pxatual, pyatual][index])[1+l::]
        # gerencia indices
        index = index + 1
        if index == 3:
            index = 0
            pxatual = pxatual + 1
        if pxatual == comprimento:
            pxatual = 0
            pyatual = pyatual + 1
    # transforma os bits salvos em caractéres alfanumércos
    out = BinParaChar(out)
    return out

# interface de teste
while not inp == "3":
    print("O que deseja fazer?")
    print("1. Encriptar uma mensagem")
    print("2. Decriptar uma mensagem")
    print("3. Sair")
    inp = input("")
    if inp == "1":
        mensagem = input("Digite a mensagem a ser encriptada: ")
        imagemBase = input("Digite o nome do arquivo bmp: ") + ".bmp"
        imagemNova = input("Digite o nome do novo arquivo bmp: ") + ".bmp"
        separador = input("Digite o separador a ser usado (caractére único, não presente na mensagem; o mesmo deverá ser usado na decriptação - eg. !, @, $): ")
        imagemE = Image.open(imagemBase)
        Encriptador(mensagem, imagemE, imagemNova, separador)
        print("")
    if inp == "2":
        imagemBase = input("Digite o nome do arquivo bmp: ") + ".bmp"
        separador = input("Digite o separador a ser usado (caractére único, não presente na mensagem; o mesmo usado na encriptação - eg. !, @, $): ")
        imagemD = Image.open(imagemBase)
        print("A mensagem escondida é: ")
        print(Decriptador(imagemD, separador))
        print("")