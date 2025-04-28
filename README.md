# Gestão de Estoque com Simulação IoT

Sistema completo de gestão de estoque, simulando um ambiente IoT com controle de estoque a partir de sensores de balança em prateleiras. O sistema é composto por backend em Flask, frontend em React utilizando Vite, banco de dados MySQL e integração com dashboard de visualização de dados via Tagorun.

### ✨ Funcionalidades
- Simulação de um sistema IoT de gerenciamento de estoque por peso
- Criação e edição de produtos e prateleiras
- Atribuição de produtos a prateleiras específicas
- Controle automático de entradas e saídas de produtos
- Atualização em tempo real da quantidade em prateleira
- Geração de alertas para níveis críticos de estoque
- Registro de histórico de movimentações
- Dashboard de visualização no Tagorun
- Integração segura com MySQL
- Interface web moderna

### 🛠️ Tecnologias Utilizadas
- Backend: Python + Flask
- Frontend: React + Vite
- Banco de Dados: MySQL
- Dashboard: Tagorun
- Gerenciamento de Ambiente: dotenv (.env)

### 🚀 Como Rodar o Projeto

# 1. Clone o repositório
```bash
# Clone o repositório
git clone https://github.com/gui1hermereis/GestaoEstoque.git
cd GestaoEstoque
```

# 2. Configure o ambiente virtual Python
```bash
python -m venv venv
Ative o ambiente:
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate    # Windows
```

# 3. Instale as dependências do backend
```bash
cd API
pip install -r requirements.txt
```

# 4. Configure o banco de dados
Antes de iniciar a API, é necessário criar manualmente um banco de dados vazio no MySQL.

Crie o banco de dados executando o comando:
```bash
CREATE DATABASE api;
```
⚡ Atenção: As tabelas necessárias serão criadas automaticamente quando a API for executada pela primeira vez, não é necessário criar as tabelas manualmente.

# 5. Baixe e configure o ngrok

Acesse ngrok.com, crie uma conta gratuita e baixe o ngrok.

Após a instalação, exponha a porta do backend (porta 5000) com o comando:
```bash
ngrok http 5000
```
Copie a URL HTTPS gerada pelo ngrok e utilize-a no campo API_URL do seu arquivo .env.

Exemplo de URL gerada: https://abc123.ngrok.io

# 6. Configure as variáveis de ambiente
Crie um arquivo .env dentro da pasta API com o seguinte conteúdo:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASS=sua_senha
DB_NAME=api
API_URL="URL gerada pelo ngrok"
```

# 7. Inicie o servidor backend
```bash
python app.py
```

# 8. Configure e inicie o frontend
```bash
cd ../frontend
npm install
npm run dev
```
📊 Integração com Dashboard (Tagorun)

Os dados de estoque são enviados e visualizados através do Tagorun, possibilitando dashboards interativos para análises em tempo real.
Acesse o dashboard de visualização de dados aqui: link

📬 Contato

Desenvolvido por Guilherme Reis 🚀
