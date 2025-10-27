# Servidor - Gerenciador de Comandas

Sistema web Flask para gerenciamento de pedidos da floricultura "Plante Uma Flor".

## 🚀 Funcionalidades

- ✅ Criação de pedidos via formulário web
- ✅ API REST para integração com cliente desktop
- ✅ Listagem e visualização de todos os pedidos
- ✅ Atualização de status (Pendente, Em Produção, Concluído)
- ✅ Deleção de pedidos
- ✅ Interface moderna e responsiva
- ✅ Banco de dados SQLite

## 📋 Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Navegue até a pasta do servidor:**
   ```bash
   cd Servidor/static
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Executando o Servidor

```bash
python app.py
```

O servidor estará disponível em: `http://localhost:5000`

Para acesso em outras máquinas da rede local: `http://192.168.0.10:5000`

## 📡 Rotas Disponíveis

### Páginas Web

- `GET /` - Página principal (listagem de pedidos)
- `GET /criar-pedido` - Formulário de criação de pedido
- `POST /criar-pedido` - Processamento do formulário

### API REST

- `POST /api/pedidos` - Criar novo pedido (JSON)
- `POST /pedido/<id>/atualizar-status` - Atualizar status
- `POST /pedido/<id>/deletar` - Deletar pedido

## 🔧 Estrutura de Dados - Modelo Pedido

```python
class Pedido:
    id: int                    # ID único (auto-incremento)
    cliente: str               # Nome do cliente
    produto: str               # Nome do produto
    quantidade: int            # Quantidade (convertido para inteiro, mínimo 0)
    status: str                # 'pendente', 'em_producao', 'concluido'
    horario: str               # Horário no formato 'HH:MM'
    dia_entrega: date          # Data no formato 'YYYY-MM-DD'
    destinatario: str          # Nome do destinatário
    mensagem: str | None       # Mensagem opcional (None se vazia)
    created_at: datetime       # Data/hora de criação
```

## 📝 Campos do Formulário

### Campos Obrigatórios:
- **cliente** (string): Nome do cliente
- **produto** (string): Nome do produto
- **quantidade** (int): Quantidade (convertido para inteiro, mínimo 0)
- **horario** (string): Horário no formato 'HH:MM'
- **dia_entrega** (date): Data no formato 'YYYY-MM-DD'
- **destinatario** (string): Nome do destinatário

### Campos Opcionais:
- **mensagem** (string): Mensagem personalizada (convertida para None se vazia)

## 🔒 Validações Implementadas

1. **Quantidade**: Convertida para inteiro, mínimo 0
2. **Mensagem**: Armazenada como `None` se vazia
3. **Data**: Formato `YYYY-MM-DD`
4. **Horário**: Formato `HH:MM` (validação com regex)
5. **Campos obrigatórios**: Verificação de preenchimento

## 🎨 Interface

- Design moderno e responsivo
- Gradientes e animações suaves
- Cards coloridos por status
- Estatísticas em tempo real
- Mensagens de feedback
- Confirmações para ações destrutivas

## 🔄 Fluxo de Trabalho

1. Acessar `/criar-pedido`
2. Preencher o formulário
3. Submeter o formulário
4. Dados são validados e convertidos
5. Pedido é salvo no banco de dados (SQLite)
6. Redirecionamento para `/` (listagem)
7. Pedidos podem ser atualizados ou deletados

## 🌐 Integração com Cliente Desktop

O servidor também atende requisições da aplicação desktop (`Clientes/PDFgen.py`) via API:

```python
# Exemplo de uso no cliente desktop
import requests

dados = {
    "nome": "João Silva",
    "produto": "Buquê 12 rosas vermelhas",
    "valor": "R$ 120,00"
}

response = requests.post("http://192.168.0.10:5000/api/pedidos", json=dados)
```

## 📦 Banco de Dados

O banco de dados SQLite (`database.db`) é criado automaticamente na pasta `static/`.

### Estrutura da Tabela `pedidos`:

```sql
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente TEXT NOT NULL,
    produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    status TEXT DEFAULT 'pendente',
    horario TEXT NOT NULL,
    dia_entrega DATE NOT NULL,
    destinatario TEXT NOT NULL,
    mensagem TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🐛 Troubleshooting

### Problema: Porta 5000 já em uso
**Solução:** Altere a porta no arquivo `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Use outra porta
```

### Problema: Erro ao criar banco de dados
**Solução:** Verifique permissões de escrita na pasta `static/`

### Problema: CORS ao acessar de outra máquina
**Solução:** O Flask já está configurado para aceitar conexões de qualquer IP (`host='0.0.0.0'`)

## 📝 Licença

Este projeto é para uso interno da Plante Uma Flor Floricultura.

## 👨‍💻 Desenvolvimento

Desenvolvido para auxiliar na gestão de pedidos da floricultura.

