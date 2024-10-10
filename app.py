from flask import Flask, render_template, request, jsonify
from abc import ABC, abstractmethod
import itertools
import random

# Cria a aplicação Flask, que será responsável por rodar o servidor web
app = Flask(__name__)

# Cria uma classe abstrata BaseMachine que serve como um modelo para outras classes
# Essa classe define métodos que devem ser implementados pelas subclasses
class BaseMachine(ABC):
    @abstractmethod
    def _gen_permutations(self):
        # Método abstrato que deverá gerar as permutações (combinações) de emojis
        ...

    @abstractmethod
    def _get_final_result(self):
        # Método abstrato para obter o resultado final da máquina de caça-níquel
        ...

    @abstractmethod
    def _display(self):
        # Método abstrato para exibir o resultado da jogada
        ...

    @abstractmethod
    def _check_result_user(self):
        # Método abstrato para verificar se o jogador ganhou ou perdeu
        ...

    @abstractmethod
    def _update_balance(self):
        # Método abstrato para atualizar o saldo do jogador após a jogada
        ...

    @abstractmethod
    def emojize(self):
        # Método abstrato para converter os códigos dos emojis em seus símbolos gráficos
        ...

    @abstractmethod
    def gain(self):
        # Método abstrato para retornar o saldo atual da máquina de caça-níquel
        ...

    @abstractmethod
    def play(self, amount_bet, player):
        # Método abstrato que representa a lógica de jogar uma rodada
        ...

# Classe que representa o jogador, armazenando o saldo e o número de vitórias
class Player:
    def __init__(self, balance=0):
        self.balance = balance  # Saldo do jogador
        self.victories = 0  # Contador de vitórias do jogador

# Classe que representa a máquina caça-níquel, herda da classe abstrata BaseMachine
class CassaNiquel(BaseMachine):
    ALL_EMOJIS = {
        'star_struck': '1F929',  # Emojis disponíveis no jogo, com seus respectivos códigos
        'zany_face': '1F92A',
        'cold_face': '1F976',
        'alien': '1F47D',
        'fire': '1F525',
        'unicorn': '1F984',
        'clown_face': '1F921',
        'ghost': '1F47B',
        'poop': '1F4A9',
        'skull': '1F480',
        'bomb': '1F4A3',
        'money_mouth_face': '1F911'
    }

    def __init__(self, level=1, balance=0):
        # Inicializa a máquina de caça-níquel com um nível e saldo
        self.level = level  # Define o nível de dificuldade
        self.SIMBOLOS = self.ALL_EMOJIS.copy()  # Copia os emojis disponíveis
        self.permutations = self._gen_permutations()  # Gera as combinações de emojis
        self.balance = balance  # Saldo da máquina

    def _gen_permutations(self):
        # Gera todas as combinações possíveis de 3 emojis diferentes
        permutations = list(itertools.product(self.SIMBOLOS.keys(), repeat=3))
        
        # Adiciona combinações extras onde todos os três emojis são iguais (para criar chances de vitória)
        for emoji in self.SIMBOLOS.keys():
            permutations.append((emoji, emoji, emoji))
        return permutations

    def _get_final_result(self):
        # Seleciona aleatoriamente uma combinação de emojis
        result = list(random.choice(self.permutations))

        # Aumenta a dificuldade de vitória conforme o nível aumenta
        if self.level > 1:
            if random.randint(0, 5) >= 3:  # Aumenta a dificuldade com base em um número aleatório
                result[1] = result[0]  # Força dois emojis a serem iguais, dificultando a vitória

        return result

    def _display(self, amount_bet, result):
        # Exibe o resultado da jogada, convertendo os códigos de emoji em símbolos gráficos
        print(self._emojize(result))
        
        # Verifica se o jogador venceu e exibe a mensagem correspondente
        if self._check_result_user(result):
            prize = amount_bet * 3 * self.level  # Calcula o prêmio
            print(f'VOCÊ VENCEU E RECEBEU: {prize}')
            return True  # Indica que o jogador venceu
        else:
            print('Foi quase, tente novamente.')
            return False  # Indica que o jogador perdeu

    def _emojize(self, emojis):
        # Converte os códigos hexadecimais dos emojis em seus símbolos gráficos
        return [chr(int(self.SIMBOLOS[emoji], 16)) for emoji in emojis]

    def _check_result_user(self, result):
        # Verifica se todos os emojis da combinação são iguais (condição de vitória)
        return all(x == result[0] for x in result)

    def _upgrade_balance(self, amount_bet, result, player: Player):
        # Atualiza o saldo do jogador e da máquina com base no resultado da jogada
        if self._check_result_user(result):
            emoji = result[0]
            # Define multiplicadores de prêmio para emojis especiais
            multiplicadores = {
                'money_mouth_face': 20,
                'fire': 15,
                'poop': 10,
                'bomb': 5
            }
            # Calcula o prêmio usando o multiplicador apropriado
            multiplicador = multiplicadores.get(emoji, 3 * self.level)
            prize = amount_bet * multiplicador  # Calcula o valor do prêmio
            player.balance += prize  # Aumenta o saldo do jogador
            player.victories += 1  # Incrementa o número de vitórias
            self.balance -= prize  # Diminui o saldo da máquina

            # Verifica se o jogador atingiu o número necessário de vitórias para subir de nível
            self._check_level_up(player)
        else:
            # Se o jogador perdeu, verifica se ele tem saldo suficiente para continuar apostando
            if player.balance >= amount_bet:
                player.balance -= amount_bet  # Deduz a aposta do saldo do jogador
            else:
                print("Saldo insuficiente!")  # Exibe uma mensagem se o jogador não tiver saldo

    def emojize(self, emojis):
        # Retorna a representação gráfica dos emojis (mesma lógica do método _emojize)
        return self._emojize(emojis)

    def gain(self):
        # Retorna o saldo da máquina
        return self.balance

    def _update_balance(self, amount_bet, result, player: Player):
        # Atualiza o saldo da máquina e do jogador com base no resultado
        self._upgrade_balance(amount_bet, result, player)

    def _check_level_up(self, player: Player):
        # Verifica se o jogador venceu 3 vezes consecutivas e, se sim, aumenta o nível
        if player.victories >= 3:
            player.victories = 0  # Reseta as vitórias
            self.level += 1  # Aumenta o nível da máquina
            print(f'PARABÉNS! Você subiu para o nível {self.level}!')

    def play(self, amount_bet, player: Player):
        # Método principal para jogar uma rodada
        result = self._get_final_result()  # Obtém o resultado da rodada
        ganhou = self._display(amount_bet, result)  # Exibe o resultado e verifica se o jogador ganhou
        self._update_balance(amount_bet, result, player)  # Atualiza o saldo da máquina e do jogador

        return result, ganhou  # Retorna o resultado e se o jogador ganhou

# Inicializa a máquina caça-níquel e o jogador
maquina1 = CassaNiquel(level=1)
player1 = Player(balance=100)  # O jogador começa com um saldo de 100

# Define a rota principal da aplicação (página inicial)
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza o arquivo index.html

# Rota para processar a jogada
@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()  # Obtém os dados enviados pelo jogador (como o valor da aposta)
    amount_bet = data.get('amount_bet')  # Pega o valor da aposta

    try:
        amount_bet = float(amount_bet)  # Converte o valor da aposta para número
    except ValueError:
        # Retorna um erro se o valor não for numérico
        return jsonify({'error': 'Valor da aposta inválido.'}), 400

    # Verifica se o valor da aposta é válido (maior que 0.24 e menor ou igual ao saldo do jogador)
    if amount_bet <= 0.24 or amount_bet > player1.balance:
        return jsonify({'error': 'Aposta inválida.'}), 400

    # Processa a jogada chamando o método play da máquina
    result, ganhou = maquina1.play(amount_bet, player1)

    # Retorna o resultado da jogada em formato JSON
    return jsonify({
        'result': maquina1._emojize(result),  # Emojis gerados
        'ganhou': ganhou,  # Se o jogador ganhou ou não
        'balance': player1.balance,  # Saldo atualizado do jogador
        'level': maquina1.level  # Nível atual da máquina
    })

# Inicia o servidor Flask em modo de debug
if __name__ == '__main__':
    app.run(debug=True)
