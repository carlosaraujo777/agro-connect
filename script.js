const API_URL = 'http://127.0.0.1:8000/api/produtos';

// 1. Função para carregar os produtos e calcular o lucro
async function carregarProdutos() {
    const resposta = await fetch(API_URL);
    const produtos = await resposta.json();
    
    const lista = document.getElementById('lista-produtos');
    lista.innerHTML = '';

    for (const produto of produtos) {
        // Busca a cotação atualizada desse produto no Back-end
        const resCotacao = await fetch(`http://127.0.0.1:8000/api/cotacao/${produto.nome}`);
        const dadosCotacao = await resCotacao.json();
        const precoSaca = dadosCotacao.preco_saca;

        // Calcula a receita e o lucro
        const receita = produto.quantidade * precoSaca;
        const lucro = receita - produto.custo;
        
        // Define a cor do texto (Verde se lucro, Vermelho se prejuízo)
        const corLucro = lucro >= 0 ? '#3fb950' : '#f85149';

        const div = document.createElement('div');
        div.className = 'produto-item';
        div.innerHTML = `
            <h3>${produto.nome}</h3>
            <p><strong>Custo de Produção:</strong> R$ ${produto.custo.toFixed(2)}</p>
            <p><strong>Quantidade:</strong> ${produto.quantidade} sacas</p>
            <p><strong>Cotação Atual (Saca):</strong> R$ ${precoSaca.toFixed(2)}</p>
            <p><strong>Receita Estimada:</strong> R$ ${receita.toFixed(2)}</p>
            <p style="color: ${corLucro}; font-weight: bold; font-size: 1.1rem; margin-top: 10px;">
                ${lucro >= 0 ? 'Lucro' : 'Prejuízo'}: R$ ${Math.abs(lucro).toFixed(2)}
            </p>
        `;
        lista.appendChild(div);
    }
}

// 2. Função para enviar um novo produto (continua igual)
document.getElementById('form-produto').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nome = document.getElementById('nome').value;
    const custo = parseFloat(document.getElementById('custo').value);
    const quantidade = parseInt(document.getElementById('quantidade').value);

    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, custo, quantidade })
    });

    document.getElementById('form-produto').reset();
    carregarProdutos();
});

// 3. Carrega a lista ao abrir a página
carregarProdutos();