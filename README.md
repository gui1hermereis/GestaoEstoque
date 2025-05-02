# Gestão de Estoque com Simulação IoT

Sistema completo de gestão de estoque, simulando um ambiente IoT com controle de estoque a partir de sensores de balança em prateleiras. O sistema é composto por backend em Python com Flask, frontend em React utilizando Vite, banco de dados MySQL e integração com dashboard de visualização de dados via Tagorun.

### ✨ Funcionalidades
- Simulação de um sistema IoT de gerenciamento de estoque por peso
- Criação, edição e exclusão de produtos e prateleiras
- Atribuição, edição e exclusão de produtos em prateleiras específicas
- Controle automático de entradas e saídas de produtos
- Atualização em tempo real da quantidade em prateleira
- Geração de alertas para níveis críticos de estoque
- Registro de histórico de movimentações
- Botão para simulação de movimentações no estoque
- Envio e exclusão automática de dados no TagoIO
- Dashboard de visualização no Tagorun
- Integração segura com MySQL
- Interface web moderna

### 🛠️ Tecnologias Utilizadas
- Backend: Python + Flask
- Frontend: React + Vite
- Banco de Dados: MySQL
- Dashboard: TagoIo + Tagorun

## 📊 Integração com Dashboard (Tagorun)
Os dados de estoque são enviados e visualizados através do Tagorun, possibilitando dashboards para análises em tempo real.

Acesse o dashboard de visualização de dados [aqui](https://680af01809d547000ad4e172.us-e1.tago.run/dashboards/info/680c19f296c409000ab2272e?anonymousToken=00000000-680a-f018-09d5-47000ad4e172)

## 🚀 Como Rodar o Projeto

## 1. Clone o repositório
```bash
# Clone o repositório
git clone https://github.com/gui1hermereis/GestaoEstoque.git
cd GestaoEstoque
```

## 2. Configure o ambiente virtual Python
```bash
cd API
python -m venv venv
# Ative o ambiente:
.\venv\Scripts\activate   # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

## 3. Instale as dependências do backend
```bash
pip install -r requirements.txt
```

## 4. Configure o banco de dados
Antes de iniciar a API, é necessário criar manualmente um banco de dados vazio no MySQL.

Crie o banco de dados executando o comando:
```bash
CREATE DATABASE api;
```
⚡ Atenção: As tabelas necessárias serão criadas automaticamente quando a API for executada pela primeira vez, não é necessário criar as tabelas manualmente.

## 5. Baixe e configure o ngrok

Acesse [ngrok.com](https://ngrok.com/), crie uma conta gratuita e baixe o ngrok.

Após a instalação, exponha a porta do backend (porta 5000) com o comando:
```bash
ngrok http 5000
```
Copie a URL HTTPS gerada pelo ngrok e utilize-a no campo API_URL do seu arquivo .env.

Exemplo de URL gerada: https://abc123.ngrok.io

## 6. Configure as variáveis de ambiente
Crie um arquivo .env dentro da pasta API com o seguinte conteúdo:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASS=sua_senha
DB_NAME=api
API_URL="URL gerada pelo ngrok"
```

## 7. Inicie o servidor backend
```bash
python app.py
```

## 8. Configure e inicie o frontend
```bash
cd ../frontend
npm install
npm run dev
```

## 📬 Contato
Desenvolvido por Guilherme Reis 🚀