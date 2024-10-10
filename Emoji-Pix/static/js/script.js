// Quando o documento estiver pronto
$(document).ready(function() {
    // Quando o botão de girar for clicado
    $('#spin-button').on('click', function() {
        const amountBet = parseFloat($('#amount_bet').val());  // Converte o valor apostado para float
        $('#result').hide(); // Oculta qualquer mensagem de resultado anterior

        // Validação do valor da aposta
        if (amountBet <= 0.24 || isNaN(amountBet) || amountBet <= 0) {  // Verifica se o valor da aposta é válido
            alert('Por favor, insira um valor de aposta válido.'); // Alerta se a aposta for inválida
            return; // Interrompe a execução se a validação falhar
        }

        // Requisição AJAX para o backend
        $.ajax({
            url: '/play', // URL para onde a requisição será enviada
            type: 'POST', // Método da requisição
            contentType: 'application/json', // Tipo de conteúdo
            data: JSON.stringify({ amount_bet: amountBet }), // Envia a aposta como JSON
            success: function(response) { // Se a requisição for bem-sucedida
                spinSlots(response.result, response.ganhou); // Gira os slots com o resultado
                $('#balance').text(response.balance); // Atualiza o saldo do jogador
                $('#player-level').text(response.level); // Atualiza o nível do jogador
            },
            error: function(xhr) { // Se houver um erro na requisição
                alert(xhr.responseJSON.error); // Mostra a mensagem de erro retornada pelo backend
            }
        });
    });
});

// Função para girar os slots e mostrar o resultado
function spinSlots(result, ganhou) {
    const slots = ['#slot1', '#slot2', '#slot3']; // Seletores dos slots
    let spinCount = 20; // Número de giros

    // Reproduz o som da roleta
    console.log("Reproduzindo som da roleta");
    const spinSound = document.getElementById('spin-sound'); // Seleciona o elemento de som
    spinSound.currentTime = 0; // Reinicia o som
    spinSound.play().catch(error => {
        console.error("Erro ao tentar reproduzir o som:", error); // Trata erros ao reproduzir som
    });

    // Gira os slots um certo número de vezes
    const interval = setInterval(() => {
        slots.forEach(slot => {
            $(slot).text(getRandomEmoji()); // Muda o slot para um emoji aleatório
        });

        spinCount--; // Decrementa o contador de giros
        if (spinCount === 0) { // Quando a contagem de giros chegar a zero
            clearInterval(interval); // Para o intervalo
            for (let i = 0; i < result.length; i++) {
                $(slots[i]).text(result[i]); // Mostra o resultado final nos slots
            }

            displayResultMessage(ganhou); // Exibe a mensagem de resultado

            // Se o jogador ganhou, chama a função para a chuva de emojis
            if (ganhou) {
                rainOfEmojis(); // Inicia a chuva de emojis
            }
        }
    }, 100); // Intervalo de 100 milissegundos entre as trocas de emoji
}

// Função para obter um emoji aleatório
function getRandomEmoji() {
    const emojis = ['🤑', '🔥', '💩', '💣', '🥶', '👽', '🦄', '🤡', '🤪', '💀']; // Emojis disponíveis
    return emojis[Math.floor(Math.random() * emojis.length)]; // Retorna um emoji aleatório
}

// Função para exibir a mensagem de resultado
function displayResultMessage(ganhou, emojiResult) {
    const message = ganhou ? 'VOCÊ VENCEU!!!!' : 'Foi quase, tente novamente.'; // Mensagem com base no resultado
    $('#result').text(message).show(); // Mostra a mensagem de resultado

    // Se o jogador ganhou, reproduz o som de vitória
    if (ganhou) {
        const vitoriaSound = document.getElementById('vitoriaSound'); // Seleciona o som de vitória
        vitoriaSound.currentTime = 0; // Reinicia o som
        vitoriaSound.play().catch(error => {
            console.error("Erro ao tentar reproduzir o som de vitória:", error); // Trata erros ao reproduzir o som
        });

        // Inicia a chuva de emojis se o jogador ganhou
        rainOfEmojis();

        // Adiciona animação de pulsação ao emoji com multiplicador
        pulsateEmoji(emojiResult);
    }

    // Oculta a mensagem após 3 segundos
    setTimeout(() => {
        $('#result').fadeOut();
    }, 3000); // 3000 milissegundos = 3 segundos
}

// Função para aplicar a animação de pulsação ao emoji
function pulsateEmoji(emoji) {
    const multipliers = ['🤑', '🔥', '💩', '💣']; // Emojis que têm multiplicador
    if (multipliers.includes(emoji)) {
        // Encontra o emoji correspondente e o multiplique
        const emojiElement = $(".emoji-column").find(`p:contains('${emoji}')`); // Seleciona o emoji
        const multiplierElement = $(".multiplier-column").find(`p:contains('x${multiplicadores[emoji]}')`); // Seleciona o multiplicador

        // Aplica animação de pulsação
        emojiElement.addClass('pulsate');
        multiplierElement.addClass('pulsate');

        // Remove a classe após a animação
        setTimeout(() => {
            emojiElement.removeClass('pulsate');
            multiplierElement.removeClass('pulsate');
        }, 1000); // Duração da pulsação
    }
}

// Função para gerar a chuva de emojis
function rainOfEmojis() {
    const emojiContainer = document.getElementById('emoji-rain'); // Seleciona o contêiner para os emojis
    const numberOfEmojis = 60; // Número de emojis a serem gerados
    const emojis = ['💰', '💵', '💸']; // Emojis de dinheiro

    for (let i = 0; i < numberOfEmojis; i++) {
        const emoji = document.createElement('div'); // Cria um novo elemento div para o emoji
        emoji.className = 'emoji'; // Adiciona a classe 'emoji'
        emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)]; // Define o emoji aleatório
        
        // Posição aleatória no topo da tela
        emoji.style.left = Math.random() * 100 + 'vw'; // Posição horizontal aleatória
        
        // Duração aleatória da animação
        const animationDuration = Math.random() * 3 + 3; // Duração entre 3 e 6 segundos
        emoji.style.animationDuration = animationDuration + 's'; // Define a duração da animação

        // Adiciona o emoji ao contêiner
        emojiContainer.appendChild(emoji);
        
        // Faz o emoji aparecer imediatamente
        emoji.style.opacity = 1; // Mantém totalmente visível
        
        // Remove o emoji após a animação
        setTimeout(() => {
            emojiContainer.removeChild(emoji); // Remove o emoji do contêiner após a animação
        }, animationDuration * 1000); // Tempo igual à duração da animação
    }
}
