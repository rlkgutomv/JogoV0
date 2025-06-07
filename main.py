import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from Recursos.funcoes import inicializarBancoDeDados
from Recursos.funcoes import escreverDados
import json
import sys
import math

pygame.init()
em_pausa = False
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Flintstones esquivo-esquivo")
icone  = pygame.image.load("Recursos/assets/icone.jpg")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
iron = pygame.image.load("Recursos/assets/Boneco.png")
fundoStart = pygame.image.load("Recursos/assets/TelaStart.png")
fundoJogo = pygame.image.load("Recursos/assets/FundoJogo.png")
fundoDead = pygame.image.load("Recursos/assets/TelaDead.png")
passaro = pygame.image.load("Recursos/assets/passaro.png")
missel = pygame.image.load("Recursos/assets/Meteoro.png")
missileSound = pygame.mixer.Sound("Recursos/assets/missile.wav")
explosaoSound = pygame.mixer.Sound("Recursos/assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("Recursos/assets/ironsound.mp3")

def tela_boas_vindas(nome):
    cinza_claro = (230, 230, 230)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if botao_iniciar.collidepoint(evento.pos):
                    return  # Sai da tela e começa o jogo

        tela.fill(cinza_claro)

        # Texto com o nome do jogador
        saudacao = fonteMenu.render(f"Bem-vindo, {nome}!", True, preto)
        tela.blit(saudacao, (400, 180))

        # Explicações simples
        explicacao1 = fonteMenu.render("Use as setas para desviar dos mísseis.", True, preto)
        explicacao2 = fonteMenu.render("Pressione ESPAÇO para pausar o jogo.", True, preto)
        tela.blit(explicacao1, (320, 220))
        tela.blit(explicacao2, (320, 250))

        # Botão para iniciar o jogo
        botao_iniciar = pygame.draw.rect(tela, (0, 150, 0), (400, 310, 200, 50), border_radius=10)
        texto_botao = fonteMenu.render("Iniciar Jogo", True, branco)
        tela.blit(texto_botao, (450, 325))

        pygame.display.update()
        relogio.tick(60)
        
def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida

    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    # Inicia o loop da interface gráfica
    root.mainloop()
    tela_boas_vindas(nome)

    

    posicaoXPersona = 500
    posicaoYPersona = 500
    movimentoXPersona  = 0
    #movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 100
    alturaPersona = 150
    larguaMissel  = 150
    alturaMissel  = 125
    dificuldade  = 30
    raio_base = 30
    bicho_x = random.randint(10, 900)
    bicho_y = random.randint(10, 600)
    bicho_vx = random.choice([-2, -1, 1, 2])
    bicho_vy = random.choice([-2, -1, 1, 2])
    tempo_direcao_bicho = pygame.time.get_ticks()


    texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
    tela.blit(texto, (15,15))
    pausar = fonteMenu.render("Press Space to Pause Game. ", True, branco)
    tela.blit(pausar, (15,35))
    instrucao = fonteMenu.render("Press Space to Pause Game", True, branco)
    tela.blit(instrucao, (750, 15))

    while True:
        global em_pausa
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                em_pausa = not em_pausa
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona            
               
        
        if posicaoXPersona < -40 :
            posicaoXPersona = -30
        elif posicaoXPersona > 900:
            posicaoXPersona = 890
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 15
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( iron, (posicaoXPersona, posicaoYPersona) )
        #Joao paulolo
        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,800)
            pygame.mixer.Sound.play(missileSound)
            
            
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        pausar = fonteMenu.render("Press Space to Pause Game. ", True, branco)
        tela.blit(pausar, (15,35))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        
        os.system("cls")
        # print( len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo") 

        if em_pausa:
            overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Tela bem escura
            tela.blit(overlay, (0, 0))

            texto_pause = pygame.font.SysFont("arial", 50).render("Jogo pausado", True, (200, 0, 0))  # Texto vermelho
            tamanho = tela.get_size()
            texto_rect = texto_pause.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2))
            tela.blit(texto_pause, texto_rect)

            pygame.display.update()

        while em_pausa:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                         em_pausa = False

        tempo = pygame.time.get_ticks() / 1000  
        raio_pulsante = int(raio_base + 10 * math.sin(tempo * 2))
        pygame.draw.circle(tela, (255, 255, 0), (950, 50), raio_pulsante)  

        # Atualizar movimento do bicho randômico
        bicho_x += bicho_vx
        bicho_y += bicho_vy

# Mudar direção a cada 1.5 segundo
        if pygame.time.get_ticks() - tempo_direcao_bicho > 1500:
            bicho_vx = random.choice([-2, -1, 1, 2])
            bicho_vy = random.choice([-2, -1, 1, 2])
            tempo_direcao_bicho = pygame.time.get_ticks()

# Limites de tela
        if bicho_x < 0 or bicho_x > 950:
             bicho_vx *= -1
        if bicho_y < 0 or bicho_y > 650:
             bicho_vy *= -1
        tela.blit(passaro, (bicho_x, bicho_y))

        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40

    # Carrega os dados do log
    try:
        with open("log.dat", "r") as f:
            log_partidas = json.load(f)
    except:
        log_partidas = {}

    # Pega os últimos 5 registros
    registros = list(log_partidas.items())[-5:]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    jogar()
                elif quitButton.collidepoint(evento.pos):
                    quit()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        # ==== Caixa cinza no canto inferior direito ====
        largura_caixa = 400
        altura_caixa = 130
        pos_x = tela.get_width() - largura_caixa - 20
        pos_y = tela.get_height() - altura_caixa - 20

        overlay = pygame.Surface((largura_caixa, altura_caixa), pygame.SRCALPHA)
        overlay.fill((200, 200, 200, 180))  # cinza com transparência
        tela.blit(overlay, (pos_x, pos_y))

        # Título
        titulo = fonteMenu.render("Últimos 5 jogos:", True, preto)
        tela.blit(titulo, (pos_x + 10, pos_y + 5))

        # Lista de partidas
        for i, (nickname, (pontos, data)) in enumerate(registros[::-1]):
            texto = fonteMenu.render(f"{i+1}. {nickname} - {pontos} pts - {data}", True, preto)
            tela.blit(texto, (pos_x + 10, pos_y + 25 + i * 20))

        # Botões
        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))

        pygame.display.update()
        relogio.tick(60) 
start()