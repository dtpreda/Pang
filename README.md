# Pang
# Projeto \<nome\>
### FPRO/MIEIC, 2019/20
### \<Fulano de Tal (up2019xxxxx@fe.up.pt)\>
### \<1MIEIC0X\> 

#### Objetivo

1. \<Criar um clone do clássico Sokoban em Pygame\>

2. \<Em alternativa... do clássico x em Pygame\>

#### Repositório de código

1) Link para o repositório do GitHub: <https://github.com/fpro-feup/public>

2) Adicionar o prof. da Unidade (ver lista em baixo) e o "Lord of the Game" (aka Ricardo Cruz):

- https://github.com/fernandocassola
- https://github.com/rpmcruz
- https://github.com/jlopes60
- https://github.com/rcamacho

#### Descrição

\<É um jogo de puzzle em que o objetivo do jogo é empurrar caixotes para um sítio indicado. 
Para empurrar o caixote é preciso ir ao outro lado empurrá-lo. 
Ou seja, se ele ficar junto à parede, a pessoa precisa de reiniciar o jogo. Estamos a utilizar os níveis do XSokoban.\>

#### UI

![UI](https://github.com/fpro-feup/public/blob/master/assigns/ui.png)

### Pacotes

- Pygame

#### Tarefas

1. **MATRIZ para os BLOCOS**
   1. 0 (vazio) 1 (bloco)
   1. desenhar
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

### \<date\>
