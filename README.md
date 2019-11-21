# Projeto Pang
### FPRO/MIEIC, 2019/20
### David Teixeira Preda (up201904726@fe.up.pt)
### 1MIEIC04

#### Objetivo

Criar um clone do jogo [Pang](https://en.wikipedia.org/wiki/Pang_(video_game)) (NES), usando também o [Bubble Trouble](https://www.miniclip.com/games/bubble-trouble/en/) como exemplo.

#### Descrição

O objetivo é eliminar as bolas do ecrã. Cada bola sub-divide-se em várias quando se dispara com ela. As bolas não podem bater no jogador.

#### UI

![UI](ui.jpg)

### Pacotes

- Pygame

#### Tarefas

1. **MATRIZ para os BLOCOS**
   1. blocos - 50x10 (done)
   1. 0 (vazio) 1 (bloco)
   1. desenhar (done)
1. **JOGADOR**
   1. desenhar: coordenadas (resolução: 50x100)
   1. mover teclas
   1. impedir que bata nos blocos
1. **BOLAS**
   1. desenhar (resolução: 12, 25, 50, 100): pos_x, pos_y, vel_x, vel_y
   1. em cada ciclo, introduzir gravidade (vel_y += 10*dt)
   1. quando atinge o solo, impulso (if pos_y > xx: pos_y = xx; vel_y += IMPULSO*tamanho)
   1. quando atinge bloco, muda de direcção (vel_x = -vel_x)
   1. colisões com o jogador (bounding box)
1. **TIROS**
   1. tecla: cria tiro em tiro_x, altura_tiro, existe_tiro
   1. desenhar se existe_tiro
   1. em cada ciclo, altura aumenta. quando atinge o tecto, existe_tiro=False
1. **FUTURO:**
   * Multi-jogador
   * diferentes tipos de tiro

### 19/nov/2019
