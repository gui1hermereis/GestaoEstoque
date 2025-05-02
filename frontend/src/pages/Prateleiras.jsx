import { useState, useEffect } from 'react';
import { FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import AlertaModal from '../components/AlertModal.jsx';

function Prateleiras() {
    const [prateleiras, setPrateleiras] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [prateleiraSelecionada, setPrateleiraSelecionada] = useState(null);
    const [formData, setFormData] = useState({
        nome: '',
        setor: ''
    });
    const [alerta, setAlerta] = useState({ show: false, tipo: '', mensagem: '' });
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [idParaExcluir, setIdParaExcluir] = useState(null);
    const [pesquisa, setPesquisa] = useState('');

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
        fetchPrateleiras();
    }, []);

    const mostrarAlerta = (tipo, mensagem) => {
        setAlerta({ show: true, tipo, mensagem });
    };

    const fecharAlerta = () => {
        setAlerta({ show: false, tipo: '', mensagem: '' });
    };

    const abrirModal = (prateleira = null) => {
        if (prateleira) {
            setPrateleiraSelecionada(prateleira);
            setFormData(prateleira);
        } else {
            setPrateleiraSelecionada(null);
            setFormData({
                nome: '',
                setor: ''
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
            if (prateleiraSelecionada) {
                response = await fetch(`http://localhost:5000/prateleiras/${prateleiraSelecionada.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
            } else {
                response = await fetch('http://localhost:5000/prateleiras', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
            }

            if (response.ok) {
                mostrarAlerta('success', 'Prateleira salva com sucesso!');
                fecharModal();
                fetchPrateleiras();
            } else {
                const errorData = await response.json();
                mostrarAlerta('error', `Erro ao salvar prateleira: ${errorData.message || 'Erro desconhecido'}`);
            }
        } catch (error) {
            console.error('Erro ao salvar prateleira:', error);
            mostrarAlerta('error', 'Erro ao salvar prateleira!');
        }
    };

    const pedirConfirmacaoExclusao = (id) => {
        setIdParaExcluir(id);
        setShowConfirmModal(true);
    };

    const confirmarExclusao = async () => {
        try {
            const response = await fetch(`http://localhost:5000/prateleiras/${idParaExcluir}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                mostrarAlerta('success', 'Prateleira excluída com sucesso!');
                fetchPrateleiras();
            } else {
                const errorData = await response.json();
                mostrarAlerta('error', `Erro ao excluir prateleira: ${errorData.message || 'Erro desconhecido'}`);
            }
        } catch (error) {
            console.error('Erro ao excluir prateleira:', error);
            mostrarAlerta('error', 'Erro ao excluir prateleira!');
        } finally {
            setShowConfirmModal(false);
            setIdParaExcluir(null);
        }
    };

    const prateleiraFiltrada = prateleiras.filter((prat) => {
        const texto = pesquisa.toLowerCase();
        return (
            prat.nome.toLowerCase().includes(texto) ||
            prat.setor.toLowerCase().includes(texto)
        );
    });

    return (
        <div id="prateleiras" className="prateleiras-container">
            <h2 className="prateleiras-header">Prateleiras</h2>

            <div className="botao-add">
                <button onClick={() => abrirModal()} className="btn btn-adicionar">
                    <FaPlus /> Adicionar Nova Prateleira
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

            <table className="prateleiras-tabela">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Setor</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {prateleiraFiltrada.map((prateleira) => (
                        <tr key={prateleira.id}>
                            <td>{prateleira.id}</td>
                            <td>{prateleira.nome}</td>
                            <td>{prateleira.setor}</td>
                            <td>
                                <button onClick={() => abrirModal(prateleira)}>
                                    <FaEdit /> Editar
                                </button>
                                <button onClick={() => pedirConfirmacaoExclusao(prateleira.id)}>
                                    <FaTrash /> Excluir
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>{prateleiraSelecionada ? 'Editar Prateleira' : 'Adicionar Prateleira'}</h3>
                        <form onSubmit={handleSubmit}>
                            <input
                                type="text"
                                name="nome"
                                placeholder="Nome da Prateleira"
                                value={formData.nome}
                                onChange={handleInputChange}
                                required
                            />
                            <input
                                type="text"
                                name="setor"
                                placeholder="Setor"
                                value={formData.setor}
                                onChange={handleInputChange}
                                required
                            />
                            <div className="modal-actions">
                                <button type="button" className="btn btn-cancelar" onClick={fecharModal}>Cancelar</button>
                                <button type="submit" className="btn btn-salvar">Salvar</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {showConfirmModal && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>Confirmar Exclusão</h3>
                        <p>Tem certeza que deseja excluir esta prateleira?</p>
                        <div className="modal-actions">
                            <button className="btn btn-cancelar" onClick={() => setShowConfirmModal(false)}>Cancelar</button>
                            <button className="btn btn-salvar" onClick={confirmarExclusao}>Sim, excluir</button>
                        </div>
                    </div>
                </div>
            )}

            {alerta.show && (
                <AlertaModal tipo={alerta.tipo} mensagem={alerta.mensagem} onClose={fecharAlerta} />
            )}
        </div>
    );
}

export default Prateleiras;
