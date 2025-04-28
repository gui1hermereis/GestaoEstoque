function AlertaModal({ tipo, mensagem, onClose }) {
    return (
        <div className="alerta-modal-overlay">
            <div className={`alerta-modal-content ${tipo}`}>
                <h3>{tipo === 'success' ? 'Sucesso!' : 'Erro!'}</h3>
                <p>{mensagem}</p>
                <button onClick={onClose} className="btn-fechar">Fechar</button>
            </div>
        </div>
    );
}

export default AlertaModal;
