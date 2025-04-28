import { useState, useEffect } from 'react';

function Alertas() {
    const [alertas, setAlertas] = useState([]);
    const [pesquisa, setPesquisa] = useState('');

    const fetchAlertas = async () => {
        try {
            const response = await fetch('http://localhost:5000/alertas/todos');
            const data = await response.json();
            setAlertas(data.data);
        } catch (error) {
            console.error('Erro ao buscar alertas:', error);
            mostrarAlerta('error', 'Erro ao buscar alertas!');
        }
    };

    useEffect(() => {
        fetchAlertas();
    }, []);

    const alertaFiltrado = alertas.filter((hist) => {
        const texto = pesquisa.toLowerCase();
        return (
            hist.tipo_alerta.toLowerCase().includes(texto) ||
            hist.nome_produto.toLowerCase().includes(texto) ||
            hist.nome_prateleira.toLowerCase().includes(texto) ||
            hist.ativo.toLowerCase().includes(texto)
        );
    });

    return (
        <div id="alertas" className="alertas-container">
            <h2 className="alertas-header">Alertas</h2>

            <div className="pesquisa">
                <input
                    type="text"
                    placeholder="Pesquisar..."
                    className="input-pesquisa"
                    value={pesquisa}
                    onChange={(e) => setPesquisa(e.target.value)}
                />
            </div>

            <table className="alertas-tabela">
                <thead>
                    <tr>
                        <th>Tipo do alerta</th>
                        <th>Produto</th>
                        <th>Prateleira</th>
                        <th>quantidade</th>
                        <th>Data</th>
                        <th>Ativo</th>
                    </tr>
                </thead>
                <tbody>
                    {alertaFiltrado.map((alerta) => (
                        <tr key={alerta.id}>
                            <td>{alerta.tipo_alerta}</td>
                            <td>{alerta.nome_produto}</td>
                            <td>{alerta.nome_prateleira}</td>
                            <td>{alerta.quantidade}</td>
                            <td>{alerta.data_hora}</td>
                            <td>{alerta.ativo}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Alertas;