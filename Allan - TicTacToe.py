import PySimpleGUI as sg
import random
from pathlib import Path

sg.change_look_and_feel('Default1')

ARQUIVO_SCORE = 'score.txt'

jogo_correndo = True

file = Path(ARQUIVO_SCORE)
if file.is_file():
    pass
else:
    file = open(ARQUIVO_SCORE, 'w')
    file.close()

class TicTacToe:
    def __init__(self):
        self.nome = ''
        self.jogador = 'X'
        self.jogador2 = 'O'
        self.computador = 'O'
        self.vitorias_consecutivas = 0
        self.current_player = random.choice([self.jogador, self.jogador2])
        self.current_player2 = self.jogador
        self.winner = None

        # layout de escolha
        layout_janela_escolha = [
            [sg.Button("2 jogadores", size=(20, 2))],
            [sg.Button('Jogar contra Computador', size=(20, 2))],
            [sg.Button('ver score', size=(20, 2))]
        ]

        # janela de escolha
        self.janela_de_escolha = sg.Window('TicTacToe', layout=(layout_janela_escolha), size=(250, 230), margins=(40,40))

        # layout 2 players
        layout2 = [
            [sg.Text('Nick: '), sg.Input(size=(30,0), key='nome')],
            [sg.Text('Você deseja ser: '),sg.Radio('X', 'escolha', default=True, key='x'), sg.Radio('O', 'escolha', key='o')],
            [sg.Button('Começar'), sg.Button('Sair')]
        ]

        # janela 2 players
        self.janela_getname = sg.Window('TicTacToe', layout=(layout2), no_titlebar=True)

        # layout jogo do 2players
        layout_jogo = [
            [sg.Text('Vez do jogador ='), sg.Text(self.current_player, key='vez')],
            [sg.Button(key='1', size=(6,3)), sg.Button(key='2', size=(6,3)), sg.Button(key='3', size=(6,3))],
            [sg.Button(key='4', size=(6,3)), sg.Button(key='5', size=(6,3)), sg.Button(key='6', size=(6,3))],
            [sg.Button(key='7', size=(6,3)), sg.Button(key='8', size=(6,3)), sg.Button(key='9', size=(6,3))],
            [sg.Button('Sair')]
        ]

        # janela jogo
        self.janela_jogo = sg.Window('TicTacToe', layout=(layout_jogo))

        # layout jogo do contra computador
        layout_jogo2= [
            [sg.Text(f'Vitorias = {self.vitorias_consecutivas}')],
            [sg.Button(key='1', size=(6,3)), sg.Button(key='2', size=(6,3)), sg.Button(key='3', size=(6,3))],
            [sg.Button(key='4', size=(6,3)), sg.Button(key='5', size=(6,3)), sg.Button(key='6', size=(6,3))],
            [sg.Button(key='7', size=(6,3)), sg.Button(key='8', size=(6,3)), sg.Button(key='9', size=(6,3))],
            [sg.Button('Sair')]
        ]

        # janela do jogo contra computador
        self.janela_jogo2 = sg.Window('TicTacToe', layout=(layout_jogo2))

    def Iniciar(self):
        while True:
            buttons, values = self.janela_de_escolha.Read()
            if buttons == None:
                break
            elif buttons == '2 jogadores':
                self.janela_de_escolha.Close()                
                self.two_players()
            elif buttons == 'Jogar contra Computador':
                self.janela_de_escolha.Close()
                self.contra_computador()
            elif buttons == 'ver score':
                pass

    def two_players(self):
        sg.popup_ok(f'jogador 1 = {self.jogador}\njogador 2 = {self.jogador2}', no_titlebar=True)
        self.game()

    def game(self):
        global jogo_correndo
        global jogadas
        jogadas = list()
        while jogo_correndo: 
            buttons, values = self.janela_jogo.Read()
            if buttons == None:
                jogo_correndo = False
            elif buttons == 'Sair':
                sair = sg.popup_ok_cancel('Você realmente deseja sair? Todo progresso será atual será perdido!', title='Sair')
                if sair == 'OK':
                    jogo_correndo = False
                    self.Iniciar()
                else:
                    pass
            elif buttons != None and buttons != 'sair':
                for num in buttons:
                    if buttons in jogadas:
                        sg.popup_ok('Lugar ja ocupado!')
                    else:
                        self.janela_jogo[str(buttons)].update((self.current_player))
                        self.flip_player()
                        self.janela_jogo.find_element('vez').update(self.current_player)
                        self.check_if_gameover(self.janela_jogo)
                        jogadas.append(buttons)

        if self.winner == 'X' or self.winner == 'O':
            sg.popup_ok(f'O VENCEDOR FOI "{self.winner}"', title='')
        elif self.winner == 'Tie':
            sg.popup_ok(f'VELHA!', title='')

    def flip_player(self):
        if self.current_player == self.jogador:
            self.current_player = self.jogador2
        else:
            self.current_player = self.jogador

    def check_if_gameover(self, janela):
        row_winner = self.check_row(janela)
        coluna_winner = self.check_colunas(janela)
        diagonal_winner = self.check_diagonal(janela)
        tie = self.check_if_tie()

        if row_winner:
            self.winner = row_winner
        elif coluna_winner:
            self.winner = coluna_winner
        elif diagonal_winner:
            self.winner = diagonal_winner
        elif tie:
            self.winner = tie
        return

    def check_row(self, janela):
        global jogo_correndo

        row1 = janela['1'].get_text() == janela['2'].get_text() == janela['3'].get_text() != ''
        row2 = janela['4'].get_text() == janela['5'].get_text() == janela['6'].get_text() != ''
        row3 = janela['7'].get_text() == janela['8'].get_text() == janela['9'].get_text() != ''

        if row1 or row2 or row3:
            jogo_correndo = False

        if row1:
            return janela['1'].get_text()
        elif row2:
            return janela['4'].get_text()
        elif row3:
            return janela['7'].get_text()

    def check_colunas(self, janela):
        global jogo_correndo

        coluna1 = janela['1'].get_text() == janela['4'].get_text() == janela['7'].get_text() != ''
        coluna2 = janela['2'].get_text() == janela['5'].get_text() == janela['8'].get_text() != ''
        coluna3 = janela['3'].get_text() == janela['6'].get_text() == janela['9'].get_text() != ''

        if coluna1 or coluna2 or coluna3:
            jogo_correndo = False
            
        if coluna1:
            return janela['1'].get_text()
        elif coluna2:
            return janela['2'].get_text()
        elif coluna3:
            return janela['3'].get_text()


    def check_diagonal(self, janela):
        global jogo_correndo

        diagonal1 = janela['1'].get_text() == janela['5'].get_text() == janela['9'].get_text() != ''
        diagonal2 = janela['7'].get_text() == janela['5'].get_text() == janela['3'].get_text() != ''
        if diagonal1 or diagonal2:
            jogo_correndo = False
            
        if diagonal1:
            return janela['1'].get_text()
        elif diagonal2:
            return janela['7'].get_text()

    def check_if_tie(self):
        global jogo_correndo
        if len(jogadas) >= 8 and (self.winner == None):
            jogo_correndo = False
            return 'Tie'

    def contra_computador(self):
        if self.get_name():
            self.jogo_contra_computador()

    def get_name(self):
        while True:
            buttons, values = self.janela_getname.Read()
            self.nome = values['nome']
            self.x = values['x']
            self.o = values['o']
            if buttons == 'Sair':
                sair = sg.popup_ok_cancel('Você realmente deseja sair?', title='Sair')
                if sair == 'OK':
                    self.janela_getname.Close()
            elif self.nome == '':
                sg.popup_ok('Preencha todos os campos!', no_titlebar=True)
            else:
                if self.x == True:
                    self.jogador = 'X'
                    self.computador = 'O'
                    self.current_player2 = self.jogador
                elif self.o == True:
                    self.jogador = 'O'
                    self.computador = 'X'
                    self.current_player2 = self.jogador
                if buttons == 'Começar':
                    self.janela_getname.Close()
                    return True

    def jogo_contra_computador(self):
        global jogo_correndo
        global jogadas
        jogadas = list()
        while jogo_correndo:
            self.buttons, values = self.janela_jogo2.Read()
            if self.buttons == None:
                jogo_correndo = False
            elif self.buttons == 'Sair':
                sair = sg.popup_ok_cancel('Você realmente deseja sair? Todo progresso será atual será perdido!', title='Sair')
                if sair == 'OK':
                    jogo_correndo = False
            elif self.buttons != None and self.buttons != 'Sair':
                for i in self.buttons:
                    if self.buttons in jogadas:
                        sg.popup('Local ja ocupado!')
                    else:
                        self.janela_jogo2[str(self.buttons)].update(self.current_player2)
                        jogadas.append(self.buttons)
                        self.flip_player2()
                        self.check_if_computer()
                        self.check_if_gameover(self.janela_jogo2)

        if self.winner == self.jogador:
            sg.popup_ok('Você foi o vencedor')
        elif self.winner == self.computador:
            sg.popup_ok('O vencedor dessa partida foi o computador')
        elif self.winner == 'Tie':
            sg.popup_ok('Velha')

    def check_if_computer(self):
        if self.current_player2 == self.computador:
            while jogo_correndo:
                choose = random.randint(1, 9)
                if str(choose) in jogadas:
                    pass
                else:
                    self.janela_jogo2[str(choose)].update(self.current_player2)
                    self.flip_player2()
                    jogadas.append(str(choose))
                    break

    def flip_player2(self):
        if self.current_player2 == self.jogador:
            self.current_player2 = self.computador
        else:
            self.current_player2 = self.jogador
                           
    def score(self):
        pass

sistema = TicTacToe()
sistema.Iniciar()