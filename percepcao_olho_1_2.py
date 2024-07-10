import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

pygame.init()

# Configurações da janela
TAMANHO_JANELA = 1024
DIMINUICAO_TAMANHO = 16  # 8 pixels a menos de cada lado
tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
pygame.display.set_caption("Quadrados Concêntricos")

# Inicialização da fonte
pygame.font.init()
fonte = pygame.font.Font(None, 36)

# Cores iniciais
preto = 0

# Inicialização dos quadrados
quadrados = [{'tamanho': TAMANHO_JANELA, 'cinza': preto}]
quadrado_atual = 0

def desenhar_quadrados(tela, quadrados):
    tela.fill((preto, preto, preto))
    for quadrado in quadrados:
        tamanho = quadrado['tamanho']
        valor_cinza = quadrado['cinza']
        retangulo = pygame.Rect((TAMANHO_JANELA - tamanho) // 2, (TAMANHO_JANELA - tamanho) // 2, tamanho, tamanho)
        pygame.draw.rect(tela, (valor_cinza, valor_cinza, valor_cinza), retangulo)
        
        # Desenha o nível de cinza ao lado do quadrado
        texto = fonte.render(f'Cinza: {valor_cinza}', True, (255, 255, 255))
    tela.blit(texto, (retangulo.centerx, retangulo.centery))

def plotar_graficos(quadrados):
    valores_cinza = [q['cinza'] for q in quadrados]
    numeros_quadrados = np.arange(1, len(valores_cinza) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Regressão de 3º grau para os valores de cinza
    p3 = Polynomial.fit(numeros_quadrados, valores_cinza, 3)
    x_fit = np.linspace(1, len(valores_cinza), 500)
    y_fit = p3(x_fit)

    # Gráfico dos valores de tom de cinza (scatter plot + regressão)
    ax1.scatter(numeros_quadrados, valores_cinza, color='gray', label='Dados')
    ax1.plot(x_fit, y_fit, color='red', label='Regressão 3º Grau')
    ax1.set_title('Valores de Cinza dos Quadrados')
    ax1.set_xlabel('Número do Quadrado')
    ax1.set_ylabel('Valor de Cinza')
    ax1.set_ylim(0, 255)
    ax1.legend()

    # Regressão de 3º grau para os incrementos
    incrementos = np.diff(valores_cinza, prepend=valores_cinza[0])
    numeros_incrementos = np.arange(1, len(incrementos) + 1)
    p3_inc = Polynomial.fit(numeros_incrementos, incrementos, 3)
    y_fit_inc = p3_inc(np.linspace(1, len(incrementos), 500))

    # Gráfico dos incrementos (plot + regressão)
    ax2.plot(numeros_incrementos, incrementos, marker='o', color='orange', label='Dados')
    ax2.plot(np.linspace(1, len(incrementos), 500), y_fit_inc, color='blue', label='Regressão 3º Grau')
    ax2.set_title('Valores dos Incrementos')
    ax2.set_xlabel('Número do Incremento')
    ax2.set_ylabel('Valor do Incremento')
    ax2.legend()

    plt.tight_layout()
    plt.show()

    # Imprimir a equação de regressão de 3º grau para valores de cinza
    coefs_cinza = p3.convert().coef
    print(f"Equação de regressão para valores de cinza: {coefs_cinza[0]:.4f} + {coefs_cinza[1]:.4f}x + {coefs_cinza[2]:.4f}x^2 + {coefs_cinza[3]:.4f}x^3")

    # Imprimir a equação de regressão de 3º grau para incrementos
    coefs_inc = p3_inc.convert().coef
    print(f"Equação de regressão para incrementos: {coefs_inc[0]:.4f} + {coefs_inc[1]:.4f}x + {coefs_inc[2]:.4f}x^2 + {coefs_inc[3]:.4f}x^3")

    # Garantir que as listas tenham o mesmo tamanho para divisão
    tamanho_minimo = min(len(valores_cinza), len(incrementos))
    valores_cinza_cortados = valores_cinza[:tamanho_minimo]
    incrementos_cortados = incrementos[:tamanho_minimo]

    # Cálculo da divisão elemento a elemento
    divisao = np.divide(incrementos_cortados, valores_cinza_cortados)

    # Cálculo de log(tom de cinza) e log(incremento/tom de cinza)
    log_cinza = np.log(valores_cinza_cortados)
    log_divisao = np.log(divisao)

    # Plotagem do resultado
    plt.figure(figsize=(6, 6))
    plt.scatter(log_divisao, log_cinza, color='green')
    plt.title('log(tom de cinza) vs log(incremento/tom de cinza)')
    plt.xlabel('log(incremento/tom de cinza)')
    plt.ylabel('log(tom de cinza)')
    plt.show()



# Loop principal
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                quadrados[quadrado_atual]['cinza'] = min(255, quadrados[quadrado_atual]['cinza'] + 1)
            elif evento.key == pygame.K_d:
                novo_tamanho = quadrados[quadrado_atual]['tamanho'] - DIMINUICAO_TAMANHO
                if novo_tamanho > 0:
                    novo_quadrado = {'tamanho': novo_tamanho, 'cinza': quadrados[quadrado_atual]['cinza']}
                    quadrados.append(novo_quadrado)
                    quadrado_atual += 1
            elif evento.key == pygame.K_s:
                plotar_graficos(quadrados)

    desenhar_quadrados(tela, quadrados)
    pygame.display.flip()

pygame.quit()
sys.exit()
