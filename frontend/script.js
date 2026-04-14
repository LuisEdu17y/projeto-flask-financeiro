const URL_BASE = 'http://127.0.0.1:5000';

// 1. Carrega Contas e Categorias automaticamente para os Selects
async function carregarOpcoesFormulario() {
    try {
        const resCat = await fetch(`${URL_BASE}/categorias`);
        const categorias = await resCat.json();
        const selectCat = document.getElementById('categoria_id');
        selectCat.innerHTML = '<option value="">Selecione a Categoria</option>';
        categorias.forEach(c => {
            selectCat.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
        });

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

        let saldoTotal = 0;

        lancamentos.forEach(lan => {
            if (lan.tipo === 'entrada') {
                saldoTotal += lan.valor;
            } else if (lan.tipo === 'saida') {
                saldoTotal -= lan.valor;
            }

            const tr = document.createElement('tr');
            const badgeClass = lan.tipo === 'entrada' ? 'tipo-entrada' : 'tipo-saida';
            const tipoFormatado = lan.tipo.charAt(0).toUpperCase() + lan.tipo.slice(1);

            // Adicionado o botão Editar que chama a função prepararEdicao passando os dados
            tr.innerHTML = `
                <td><strong>${lan.descricao}</strong></td>
                <td>ID ${lan.categoria_id} (Automático)</td>
                <td>R$ ${lan.valor.toFixed(2)}</td>
                <td><span class="badge-tipo ${badgeClass}">${tipoFormatado}</span></td>
                <td>
                    <button class="btn-editar" style="background-color: #f39c12; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-right: 5px;" 
                        onclick="prepararEdicao(${lan.id}, '${lan.descricao}', ${lan.valor}, '${lan.tipo}', ${lan.categoria_id}, ${lan.conta_id})">
                        Editar
                    </button>
                    <button class="btn-apagar" onclick="apagarLancamento(${lan.id})">Apagar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        const elementoSaldo = document.getElementById('valor-saldo');
        if (elementoSaldo) {
            elementoSaldo.innerText = `R$ ${saldoTotal.toFixed(2)}`;
            if (saldoTotal < 0) {
                elementoSaldo.style.color = '#e74c3c';
            } else {
                elementoSaldo.style.color = '#4CAF50';
            }
        }

    } catch (erro) {
        console.error("Erro ao carregar lançamentos:", erro);
    }
}

// NOVO: Função para colocar os dados da tabela de volta no formulário
function prepararEdicao(id, descricao, valor, tipo, categoria_id, conta_id) {
    document.getElementById('edit-id').value = id; // Preenche o campo oculto
    document.getElementById('descricao').value = descricao;
    document.getElementById('valor').value = valor;
    document.getElementById('tipo').value = tipo;
    document.getElementById('categoria_id').value = categoria_id;
    document.getElementById('conta_id').value = conta_id;

    // Altera o botão para dar feedback visual ao usuário
    const btnSubmit = document.querySelector('#form-lancamento button[type="submit"]');
    btnSubmit.innerText = "Salvar Alterações";
    btnSubmit.style.backgroundColor = "#f39c12";

    // Rola a página para o formulário (opcional, para conveniência)
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 3. Salva ou Atualiza um Lançamento
document.getElementById('form-lancamento').addEventListener('submit', async function(evento) {
    evento.preventDefault(); 
    
    // Verifica se temos um ID no campo oculto (se tiver, é uma edição)
    const idParaEditar = document.getElementById('edit-id').value;
    
    const dados = {
        descricao: document.getElementById('descricao').value,
        valor: parseFloat(document.getElementById('valor').value),
        tipo: document.getElementById('tipo').value,
        usuario_id: parseInt(document.getElementById('usuario_id').value),
        conta_id: parseInt(document.getElementById('conta_id').value),
        categoria_id: parseInt(document.getElementById('categoria_id').value)
    };

    // Define a URL e o Método dependendo se é Edição ou Criação
    const url = idParaEditar ? `${URL_BASE}/lancamentos/${idParaEditar}` : `${URL_BASE}/lancamentos`;
    const metodo = idParaEditar ? 'PUT' : 'POST';

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            document.getElementById('mensagem-erro').innerText = "";
            document.getElementById('form-lancamento').reset();
            
            // Limpa o ID de edição e volta o botão ao normal
            document.getElementById('edit-id').value = "";
            const btnSubmit = document.querySelector('#form-lancamento button[type="submit"]');
            btnSubmit.innerText = "Registrar Lançamento";
            btnSubmit.style.backgroundColor = ""; // Volta para a cor original do CSS

            carregarLancamentos(); 
        } else {
            document.getElementById('mensagem-erro').innerText = "Erro: " + (resultado.erro || "Falha ao processar");
        }
    } catch (erro) {
        console.error("Erro ao salvar/atualizar:", erro);
    }
});

// 4. Apagar Lançamento
async function apagarLancamento(id) {
    if (confirm("Deseja realmente excluir este registro?")) {
        await fetch(`${URL_BASE}/lancamentos/${id}`, { method: 'DELETE' });
        carregarLancamentos();
    }
}

// Inicia as funções quando a tela abre
carregarOpcoesFormulario();
carregarLancamentos();