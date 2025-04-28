import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Produtos from '../src/pages/Produtos';
import Prateleiras from '../src/pages/Prateleiras';
import PrateleirasProdutos from './pages/PrateleirasProdutos';
import Historico from './pages/Historico';
import Alertas from './pages/Alertas';
import '../src/css/App.css';

function App() {
  return (
    <Router>
      <div>
        <header className="header">
          <h1>Gestão De Estoque</h1>
        </header>

        <nav className="navbar">
          <a href="/produtos">Produtos</a>
          <a href="/prateleiras">Prateleiras</a>
          <a href="/prateleirasProdutos">Estoque</a>
          <a href="/alertas">Alertas</a>
          <a href="/historico">Historico</a>
        </nav>

        <Routes>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<Home />} />
          <Route path="/produtos" element={<Produtos />} />
          <Route path="/prateleiras" element={<Prateleiras />} />
          <Route path="/prateleirasProdutos" element={<PrateleirasProdutos />} />
          <Route path="/alertas" element={<Alertas />} />
          <Route path="/historico" element={<Historico />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
