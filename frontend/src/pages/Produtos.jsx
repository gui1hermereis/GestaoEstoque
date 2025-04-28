import { useState, useEffect } from 'react';
import { FaPlus, FaBox, FaEdit, FaTrash } from 'react-icons/fa';
import AlertaModal from '../components/AlertModal.jsx';

function Produtos() {
    const [produtos, setProdutos] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [produtoSelecionado, setProdutoSelecionado] = useState(null);
    const [formData, setFormData] = useState({
        marca: '',
        nome: '',
        descricao: '',
        peso: '',
        preco_unidade: ''
    });
    const [alerta, setAlerta] = useState({ show: false, tipo: '', mensagem: '' });
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [idParaExcluir, setIdParaExcluir] = useState(null);
    const [pesquisa, setPesquisa] = useState('');

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

    useEffect(() => {
        fetchProdutos();
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
            setFormData(produto);
        } else {
            setProdutoSelecionado(null);
            setFormData({
                marca: '',
                nome: '',
                descricao: '',
                peso: '',
                preco_unidade: ''
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
            if (produtoSelecionado) {
                response = await fetch(`http://localhost:5000/produtos/${produtoSelecionado.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
            } else {
                response = await fetch('http://localhost:5000/produtos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
            }

            if (response.ok) {
                mostrarAlerta('success', 'Produto salvo com sucesso!');
                fecharModal();
                fetchProdutos();
            } else {
                const errorData = await response.json();
                mostrarAlerta('error', `Erro ao salvar produto: ${errorData.message || 'Erro desconhecido'}`);
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
            const response = await fetch(`http://localhost:5000/produtos/${idParaExcluir}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                mostrarAlerta('success', 'Produto excluído com sucesso!');
                fetchProdutos();
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

    const produtoFiltrado = produtos.filter((prod) => {
        const texto = pesquisa.toLowerCase();
        return (
            prod.marca.toLowerCase().includes(texto) ||
            prod.nome.toLowerCase().includes(texto) ||
            prod.descricao.toLowerCase().includes(texto)
        );
    });

    return (
        <div id="produtos" className="produtos-container">
            <h2 className="produtos-header">Produtos</h2>
            <div className="botao-add">
                <button onClick={() => abrirModal()} className="btn btn-adicionar">
                    <FaPlus /> Adicionar Novo Produto
                </button>
            </div>

            <div className="pesquisa">
                <input
                    type="text"
                    placeholder="Pesquisar..."
                    className="input-pesquisa"
                    value={pesquisa}
                    onChange={(e) => setPesquisa(e.target.value)}
                />
            </div>
            <table className="produtos-tabela">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Marca</th>
                        <th>Nome</th>
                        <th>Descrição</th>
                        <th>Peso</th>
                        <th>Preço</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {produtoFiltrado.map((produto) => (
                        <tr key={produto.id}>
                            <td>{produto.id}</td>
                            <td>{produto.marca}</td>
                            <td>{produto.nome}</td>
                            <td>{produto.descricao}</td>
                            <td>{produto.peso}g</td>
                            <td>R$ {produto.preco_unidade}</td>
                            <td>
                                <div className="btn-edit">
                                    <button onClick={() => abrirModal(produto)}>
                                        <FaEdit /> Editar
                                    </button>
                                </div>
                                <div className="btn-delete">
                                    <button onClick={() => pedirConfirmacaoExclusao(produto.id)}>
                                        <FaTrash /> Excluir
                                    </button>
                                </div>

                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {
                showModal && (
                    <div className="modal">
                        <div className="modal-content">
                            <h3>{produtoSelecionado ? 'Editar Produto' : 'Adicionar Produto'}</h3>
                            <form onSubmit={handleSubmit}>
                                <input
                                    type="text"
                                    name="marca"
                                    placeholder="Marca"
                                    value={formData.marca}
                                    onChange={handleInputChange}
                                    required
                                    className="input-modal"
                                />
                                <input
                                    type="text"
                                    name="nome"
                                    placeholder="Nome"
                                    value={formData.nome}
                                    onChange={handleInputChange}
                                    required
                                    className="input-modal"
                                />
                                <textarea
                                    name="descricao"
                                    placeholder="Descrição"
                                    value={formData.descricao}
                                    onChange={handleInputChange}
                                    required
                                    className="input-modal"
                                />
                                <input
                                    type="number"
                                    name="peso"
                                    placeholder="Peso (g)"
                                    value={formData.peso}
                                    onChange={handleInputChange}
                                    required
                                    className="input-modal"
                                />
                                <input
                                    type="number"
                                    step="0.01"
                                    name="preco_unidade"
                                    placeholder="Preço (R$)"
                                    value={formData.preco_unidade}
                                    onChange={handleInputChange}
                                    required
                                    className="input-modal"
                                />
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
                            <p>Tem certeza que deseja excluir este produto?</p>
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

export default Produtos;