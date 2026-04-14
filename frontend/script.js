const URL_BASE = 'http://127.0.0.1:5000';

// 1. Carrega Contas e Categorias automaticamente para os Selects
async function carregarOpcoesFormulario() {
    try {
        // Busca Categorias
        const resCat = await fetch(`${URL_BASE}/categorias`);
        const categorias = await resCat.json();
        const selectCat = document.getElementById('categoria_id');
        selectCat.innerHTML = '<option value="">Selecione a Categoria</option>';
        categorias.forEach(c => {
            selectCat.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
        });

        // Busca Contas
        const resContas = await fetch(`${URL_BASE}/contas`);
        const contas = await resContas.json();
        const selectConta = document.getElementById('conta_id');
        selectConta.innerHTML = '<option value="">Selecione a Conta</option>';
        contas.forEach(c => {
            selectConta.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
        });
    } catch (erro) {
        console.error("Erro ao carregar opções:", erro);
    }
}

// 2. Carrega os Lançamentos para a Tabela e Calcula o Saldo
async function carregarLancamentos() {
    try {
        const resposta = await fetch(`${URL_BASE}/lancamentos`);
        const lancamentos = await resposta.json();
        
        const tbody = document.querySelector('#tabela-lancamentos tbody');
        tbody.innerHTML = ''; 

        // Variável para armazenar o saldo
        let saldoTotal = 0;

        lancamentos.forEach(lan => {
            // Lógica do Saldo: Soma se for entrada, subtrai se for saída
            if (lan.tipo === 'entrada') {
                saldoTotal += lan.valor;
            } else if (lan.tipo === 'saida') {
                saldoTotal -= lan.valor;
            }

            const tr = document.createElement('tr');
            
            // Tratamento visual para o tipo
            const badgeClass = lan.tipo === 'entrada' ? 'tipo-entrada' : 'tipo-saida';
            const tipoFormatado = lan.tipo.charAt(0).toUpperCase() + lan.tipo.slice(1);

            tr.innerHTML = `
                <td><strong>${lan.descricao}</strong></td>
                <td>ID ${lan.categoria_id} (Automático)</td>
                <td>R$ ${lan.valor.toFixed(2)}</td>
                <td><span class="badge-tipo ${badgeClass}">${tipoFormatado}</span></td>
                <td><button class="btn-apagar" onclick="apagarLancamento(${lan.id})">Apagar</button></td>
            `;
            tbody.appendChild(tr);
        });

        // Atualiza o valor do saldo no HTML
        const elementoSaldo = document.getElementById('valor-saldo');
        if (elementoSaldo) {
            elementoSaldo.innerText = `R$ ${saldoTotal.toFixed(2)}`;
            
            // Muda a cor dependendo se o saldo é positivo ou negativo
            if (saldoTotal < 0) {
                elementoSaldo.style.color = '#e74c3c'; // Vermelho para negativo
            } else {
                elementoSaldo.style.color = '#4CAF50'; // Verde para positivo
            }
        }

    } catch (erro) {
        console.error("Erro ao carregar lançamentos:", erro);
    }
}

// 3. Salva um Novo Lançamento
document.getElementById('form-lancamento').addEventListener('submit', async function(evento) {
    evento.preventDefault(); 
    
    const dados = {
        descricao: document.getElementById('descricao').value,
        valor: parseFloat(document.getElementById('valor').value),
        tipo: document.getElementById('tipo').value,
        usuario_id: parseInt(document.getElementById('usuario_id').value), // ID 1 escondido
        conta_id: parseInt(document.getElementById('conta_id').value), // Vem do select dinâmico
        categoria_id: parseInt(document.getElementById('categoria_id').value) // Vem do select dinâmico
    };

    try {
        const resposta = await fetch(`${URL_BASE}/lancamentos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            document.getElementById('mensagem-erro').innerText = "";
            document.getElementById('form-lancamento').reset();
            carregarLancamentos(); // Como isto chama a função, o saldo atualiza na hora!
        } else {
            document.getElementById('mensagem-erro').innerText = "Erro: " + (resultado.erro || "Falha ao salvar");
        }
    } catch (erro) {
        console.error("Erro ao salvar:", erro);
    }
});

// 4. Apagar Lançamento
async function apagarLancamento(id) {
    if (confirm("Deseja realmente excluir este registro?")) {
        await fetch(`${URL_BASE}/lancamentos/${id}`, { method: 'DELETE' });
        carregarLancamentos(); // Aqui também atualiza o saldo na hora!
    }
}

// Inicia as funções quando a tela abre
carregarOpcoesFormulario();
carregarLancamentos();