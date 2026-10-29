import struct



# Pôr os valores na nova imagem

def obter_matriz(file_path):
    with open(file_path, 'rb') as f:
        cabecalho = f.read(54)
        
        # Verifica se é um arquivo válido
        if cabecalho[:2] != b'BM':
            return "A imagem não é um BMP válido."
        
        offset_pixels = struct.unpack('<I', cabecalho[10:14])[0]
         
        # '<ii' = dois inteiros de 32 bits com sinal em Little-Endian
        largura, altura = struct.unpack('<ii', cabecalho[18:26])
        
        largura_bytes = ((largura * 3 + 3) // 4) * 4
        
        # Verifica se a imagem é invertida
        invertida = altura > 0      
        altura = abs(altura)
        
        f.seek(offset_pixels)
        pixels_rgb = f.read(altura * largura_bytes)
        
        imagem_matriz = []
        
        for y in range(altura):
            linha_invertida = (altura - 1 - y) if invertida else y
            linha = linha_invertida * largura_bytes
            
            linha_pixels = []
            
            for x in range(largura):
                posicao = linha + (x * 3) # São vai de 3 em 3
                
                b = pixels_rgb[posicao]
                g = pixels_rgb[posicao + 1]
                r = pixels_rgb[posicao + 2]
                
                linha_pixels.append([b, g, r])
                
            imagem_matriz.append(linha_pixels)
         
        return imagem_matriz

def filtro_grayscale(img_matriz):
    for linha in img_matriz:
        for pixel in linha:
            media = (pixel[0] + pixel[1] + pixel[2]) // 3
            
            pixel[0], pixel[1], pixel[2] = media, media, media
            
    return img_matriz


def salvar_img(img_matriz):
    with open('imagem_teste.bmp', 'rb') as f:
        cabecalho_arquivo = f.read(14)
        cabecalho_info = f.read(40)
        
        offset_pixels = struct.unpack('<I', cabecalho_arquivo[10:14])[0]
        largura, altura = struct.unpack('<ii', cabecalho_info[4:12])
        
        f.seek(0)
        cabecalhos_completos = f.read(offset_pixels)
        
    invertida = altura > 0
    altura = abs(altura)
    largura_bytes = ((largura * 3 + 3) // 4) * 4

    novos_dados_pixels = bytearray()

    for y in range(altura):
        # Ajusta a ordem das linhas de acordo com a orientação original do BMP
        linha_invertida = (altura - 1 - y) if invertida else y
        linha = img_matriz[linha_invertida]
        
        linha_bytes = bytearray()
        for pixel in linha:
            b, g, r = pixel
            linha_bytes.extend([b, g, r])
            
        # Adiciona o padding (preenchimento para múltiplo de 4 bytes)
        while len(linha_bytes) < largura_bytes:
            linha_bytes.append(0)
            
        novos_dados_pixels.extend(linha_bytes)

    # 3. Salva o novo arquivo BMP no disco
    with open('imagem_teste_grayscale.bmp', 'wb') as f:
        f.write(cabecalhos_completos)
        f.write(novos_dados_pixels)


img_matriz = obter_matriz('imagem_teste.bmp')
filtro_grayscale(img_matriz)
salvar_img(img_matriz)
 