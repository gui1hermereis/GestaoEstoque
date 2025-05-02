import { useState, useEffect } from 'react';

function Historico() {
    const [historico, setHistorico] = useState([]);
    const [pesquisa, setPesquisa] = useState('');
    const fetchHistorico = async () => {
        try {
            const response = await fetch('http://localhost:5000/historico');
            const data = await response.json();
            setHistorico(data.data);
        } catch (error) {
            console.error('Erro ao buscar historico:', error);
            mostrarAlerta('error', 'Erro ao buscar historico!');
        }
    };

    useEffect(() => {
        fetchHistorico();
    }, []);

    const historicoFiltrado = historico.filter((hist) => {
        const texto = pesquisa.toLowerCase();
        return (
            hist.nome_produto.toLowerCase().includes(texto) ||
            hist.marca.toLowerCase().includes(texto) ||
            hist.nome_prateleira.toLowerCase().includes(texto) ||
            hist.setor.toLowerCase().includes(texto) ||
            hist.tipo_movimentacao.toLowerCase().includes(texto)
        );
    });

    return (
        <div id="historico" className="historico-container">
            <h2 className="historico-header">Histórico</h2>

            <div className="pesquisa">
                <input
                    type="text"
                    placeholder="Pesquisar..."
                    className="input-pesquisa"
                    value={pesquisa}
                    onChange={(e) => setPesquisa(e.target.value)}
                />
            </div>

            <table className="historico-tabela">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Marca</th>
                        <th>Prateleira</th>
                        <th>Setor</th>
                        <th>Quantidade</th>
                        <th>Valor total</th>
                        <th>Data</th>
                        <th>Tipo de movimentação</th>
                    </tr>
                </thead>
                <tbody>
                    {historicoFiltrado.map((hist) => (
                        <tr key={hist.id}>
                            <td>{hist.nome_produto}</td>
                            <td>{hist.marca}</td>
                            <td>{hist.nome_prateleira}</td>
                            <td>{hist.setor}</td>
                            <td>{hist.quantidade}</td>
                            <td>R$ {hist.preco_total}</td>
                            <td>{hist.data_hora}</td>
                            <td>{hist.tipo_movimentacao}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Historico;