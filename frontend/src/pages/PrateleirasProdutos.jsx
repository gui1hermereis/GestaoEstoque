import { useState, useEffect } from 'react';
import { FaPlus, FaEdit, FaTrash, FaTimes } from 'react-icons/fa';
import AlertaModal from '../components/AlertModal.jsx';

function PrateleirasProdutos() {
    const [prateleirasProdutos, setPrateleirasProdutos] = useState([]);
    const [produtos, setProdutos] = useState([]);
    const [prateleiras, setPrateleiras] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [produtoSelecionado, setProdutoSelecionado] = useState(null);
    const [formData, setFormData] = useState({
        produto_id: '',
        prateleira_id: '',
        quantidade: '',
        quantidade_min: ''
    });
    const [alerta, setAlerta] = useState({ show: false, tipo: '', mensagem: '' });
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [idParaExcluir, setIdParaExcluir] = useState(null);
    const [pesquisa, setPesquisa] = useState('');

    const fetchPrateleirasProdutos = async () => {
        try {
            const response = await fetch('http://localhost:5000/prateleiras_produtos');
            const data = await response.json();
            setPrateleirasProdutos(data.data);
        } catch (error) {
            console.error('Erro ao buscar prateleiras_produtos:', error);
            mostrarAlerta('error', 'Erro ao buscar prateleiras!');
        }
    };

    const fetchProdutos = async () => {
        try {
            const response = await fetch('http://localhost:5000/produtos');
            const data = await response.json();
            setProdutos(data.produtos);
        } catch (error) {
            console.error('Erro ao buscar produtos:', error);
            mostrarAlerta('error', 'Erro ao buscar produtos!');
        }
    };

    const fetchPrateleiras = async () => {
        try {
            const response = await fetch('http://localhost:5000/prateleiras');
            const data = await response.json();
            setPrateleiras(data.Prateleiras);
        } catch (error) {
            console.error('Erro ao buscar prateleiras:', error);
            mostrarAlerta('error', 'Erro ao buscar prateleiras!');
        }
    };

    useEffect(() => {
        fetchPrateleirasProdutos();
        fetchProdutos();
        fetchPrateleiras();
    }, []);

    const mostrarAlerta = (tipo, mensagem) => {
        setAlerta({ show: true, tipo, mensagem });
    };

    const fecharAlerta = () => {
        setAlerta({ show: false, tipo: '', mensagem: '' });
    };

    const abrirModal = (produto = null) => {
        if (produto) {
            setProdutoSelecionado(produto);
            setFormData({
                produto_id: produto.produto_id,
                prateleira_id: produto.prateleira_id,
                quantidade: produto.quantidade,
                quantidade_min: produto.quantidade_min
            });
            console.log(prateleirasProdutos)
        } else {
            setProdutoSelecionado(null);
            setFormData({
                produto_id: '',
                prateleira_id: '',
                quantidade: '',
                quantidade_min: ''
            });
        }
        setShowModal(true);
    };

    const fecharModal = () => {
        setShowModal(false);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            let response;
            let { produto_id, prateleira_id, quantidade, quantidade_min } = formData;

            quantidade = parseInt(quantidade);
            quantidade_min = parseInt(quantidade_min);

            if (isNaN(quantidade) || isNaN(quantidade_min)) {
                mostrarAlerta('error', 'Quantidade e Quantidade Mínima devem ser números inteiros válidos.');
                return;
            }

            const body = { produto_id, prateleira_id, quantidade, quantidade_min };

            if (produtoSelecionado) {
                response = await fetch(`http://localhost:5000/prateleiras_produtos/${produtoSelecionado.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
            } else {
                response = await fetch('http://localhost:5000/prateleiras_produtos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
            }

            if (response.ok) {
                mostrarAlerta('success', 'Produto salvo com sucesso!');
                fecharModal();
                fetchPrateleirasProdutos();
            } else {
                const errorData = await response.json();
                mostrarAlerta('error', `Erro ao salvar produto: ${errorData.message || 'Erro desconhecido'}`);
                console.log(produtoSelecionado.id)
            }
        } catch (error) {
            console.error('Erro ao salvar produto:', error);
            mostrarAlerta('error', 'Erro ao salvar produto!');
        }
    };

    const pedirConfirmacaoExclusao = (id) => {
        setIdParaExcluir(id);
        setShowConfirmModal(true);
    };

    const confirmarExclusao = async () => {
        try {
            const response = await fetch(`http://localhost:5000/prateleiras_produtos/${idParaExcluir}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                mostrarAlerta('success', 'Produto excluído com sucesso!');
                fetchPrateleirasProdutos();
            } else {
                const errorData = await response.json();
                mostrarAlerta('error', `Erro ao excluir produto: ${errorData.message || 'Erro desconhecido'}`);
            }
        } catch (error) {
            console.error('Erro ao excluir produto:', error);
            mostrarAlerta('error', 'Erro ao excluir produto!');
        } finally {
            setShowConfirmModal(false);
            setIdParaExcluir(null);
        }
    };

    const produtosFiltrados = prateleirasProdutos.filter((estoque) => {
        const texto = pesquisa.toLowerCase();
        return (
            estoque.nome_produto?.toLowerCase().includes(texto) ||
            estoque.marca?.toLowerCase().includes(texto) ||
            estoque.nome_prateleira?.toLowerCase().includes(texto) ||
            estoque.setor?.toLowerCase().includes(texto)
        );
    });

    const [simulando, setSimulando] = useState(false);
    const [intervalId, setIntervalId] = useState(null);

    const simularBalanca = () => {
        if (!simulando) {
            const id = setInterval(async () => {
                if (prateleirasProdutos.length === 0) return;

                const registroAleatorio = prateleirasProdutos[Math.floor(Math.random() * prateleirasProdutos.length)];

                const quantidade = Math.floor(Math.random() * 5) + 1;
                const acao = Math.random() < 0.5 ? 'adicionar' : 'retirar';

                const endpoint = acao === 'adicionar'
                    ? 'http://localhost:5000/balanca/adicionar_produto'
                    : 'http://localhost:5000/balanca/retirar_produto';

                const payload = {
                    produto_id: registroAleatorio.produto_id,
                    prateleira_id: registroAleatorio.prateleira_id,
                    quantidade: quantidade
                };

                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();
                    console.log(`[${acao.toUpperCase()}] Produto ${payload.produto_id} Prateleira ${payload.prateleira_id} Quantidade ${payload.quantidade}`, data);

                    fetchPrateleirasProdutos();
                } catch (error) {
                    console.error('Erro na simulação:', error);
                }
            }, 3000);

            setIntervalId(id);
            setSimulando(true);
        } else {
            clearInterval(intervalId);
            setSimulando(false);
        }
    };

    return (
        <div id="prateleiras-produtos" className="prateleiras-produtos-container">
            <div className="prateleiras-produtos-topo">
                <div className="pesquisa">
                    <input
                        type="text"
                        placeholder="Pesquisar..."
                        className="input-pesquisa"
                        value={pesquisa}
                        onChange={(e) => setPesquisa(e.target.value)}
                    />
                </div>
                <div className="botao-simulacao">
                    <h2 className="prateleiras-produtos-header">Estoque</h2>
                    <button onClick={simularBalanca} className={`btn ${simulando ? 'btn-parar' : 'btn-simular'}`}>
                        {simulando ? 'Parar Simulação' : 'Iniciar Simulação'}
                    </button>
                </div>
                <div className="botao-add">
                    <button onClick={() => abrirModal()} className="btn btn-adicionar">
                        <FaPlus /> Adicionar Produto a Prateleira
                    </button>
                </div>
            </div>

            <table className="prateleiras-produtos-tabela">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Marca</th>
                        <th>Produto</th>
                        <th>Prateleira</th>
                        <th>Setor</th>
                        <th>Peso</th>
                        <th>Preço</th>
                        <th>Quantidade</th>
                        <th>Quantidade Mínima</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {produtosFiltrados.map((estoque) => (
                        <tr key={estoque.id}>
                            <td>{estoque.id}</td>
                            <td>{estoque.marca}</td>
                            <td>{estoque.nome_produto}</td>
                            <td>{estoque.nome_prateleira}</td>
                            <td>{estoque.setor}</td>
                            <td>{estoque.peso_atual}g</td>
                            <td>R${estoque.preco_total}</td>
                            <td>{estoque.quantidade}</td>
                            <td>{estoque.quantidade_min}</td>
                            <td>
                                <button onClick={() => abrirModal(estoque)}>
                                    <FaEdit /> Editar
                                </button>
                                <button onClick={() => pedirConfirmacaoExclusao(estoque.id)}>
                                    <FaTrash /> Excluir
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {
                showModal && (
                    <div className="modal">
                        <div className="modal-content">
                            <h3>{produtoSelecionado ? 'Editar Produto na Prateleira' : 'Adicionar Produto na Prateleira'}</h3>
                            <form onSubmit={handleSubmit}>
                                <select name="produto_id" value={formData.produto_id} onChange={handleInputChange} required>
                                    <option value="">Selecione o Produto</option>
                                    {produtos.map((produto) => (
                                        <option key={produto.id} value={produto.id}>{produto.nome}</option>
                                    ))}
                                </select>

                                <select name="prateleira_id" value={formData.prateleira_id} onChange={handleInputChange} required>
                                    <option value="">Selecione a Prateleira</option>
                                    {prateleiras.map((prateleira) => (
                                        <option key={prateleira.id} value={prateleira.id}>{prateleira.nome}</option>
                                    ))}
                                </select>
                                <input type="number" name="quantidade" placeholder="Quantidade" value={formData.quantidade} onChange={handleInputChange} required />
                                <input type="number" name="quantidade_min" placeholder="Quantidade Mínima" value={formData.quantidade_min} onChange={handleInputChange} required />
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-cancelar" onClick={fecharModal}>Cancelar</button>
                                    <button type="submit" className="btn btn-salvar">Salvar</button>
                                </div>
                            </form>
                        </div>
                    </div>
                )
            }

            {
                showConfirmModal && (
                    <div className="modal">
                        <div className="modal-content">
                            <h3>Confirmar Exclusão</h3>
                            <p>Tem certeza que deseja excluir?</p>
                            <div className="modal-actions">
                                <button className="btn btn-cancelar" onClick={() => setShowConfirmModal(false)}>Cancelar</button>
                                <button className="btn btn-salvar" onClick={confirmarExclusao}>Sim, excluir</button>
                            </div>
                        </div>
                    </div>
                )
            }

            {
                alerta.show && (
                    <AlertaModal tipo={alerta.tipo} mensagem={alerta.mensagem} onClose={fecharAlerta} />
                )
            }
        </div >
    );
}

export default PrateleirasProdutos;
