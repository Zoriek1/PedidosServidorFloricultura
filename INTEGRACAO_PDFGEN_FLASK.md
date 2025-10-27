# 🔗 Integração PDFgen ↔️ Servidor Flask

## 📋 Visão Geral

O **PDFgen** (Cliente Desktop) e o **Servidor Flask** trabalham em conjunto para gerenciar pedidos:

1. PDFgen gera o PDF do pedido
2. PDFgen envia dados via POST para o Flask
3. Flask valida e armazena no banco de dados
4. Flask responde com sucesso (200) ou erro (400)

---

## 🔄 Fluxo de Dados

```
┌──────────────────┐
│   PDFgen (Cli)  │
│   Gera PDF      │
└────────┬─────────┘
         │
         │ POST /api/pedidos
         │ {cliente, produto, 
         │  quantidade, horario,
         │  dia_entrega, destinatario,
         │  mensagem}
         ▼
┌──────────────────┐
│  Flask (Server)  │
│  Valida dados    │
│  Salva no DB     │
└────────┬─────────┘
         │
         │ Resposta
         │ {success: true,
         │  pedido_id: 123,
         │  message: "..."}
         ▼
┌──────────────────┐
│   PDFgen (Cli)  │
│   Exibe sucesso │
└──────────────────┘
```

---

## 📡 API do Servidor Flask

### Endpoint: `POST /api/pedidos`

**URL:** `http://192.168.0.10:5000/api/pedidos`

**Método:** POST

**Content-Type:** `application/json`

### Dados de Entrada (JSON)

```json
{
  "cliente": "João Silva",
  "produto": "Buquê 12 rosas vermelhas",
  "quantidade": 1,
  "horario": "14:30",
  "dia_entrega": "2024-12-25",
  "destinatario": "Maria Santos",
  "mensagem": "Feliz Aniversário!"
}
```

#### Campos Obrigatórios:
- ✅ **cliente** (string): Nome do cliente
- ✅ **produto** (string): Nome do produto
- ✅ **horario** (string): Formato `HH:MM` (ex: 14:30)
- ✅ **dia_entrega** (string): Formato `YYYY-MM-DD` (ex: 2024-12-25)
- ✅ **destinatario** (string): Nome do destinatário

#### Campos Opcionais:
- ⚪ **quantidade** (integer): Quantidade (padrão: 1 se não enviado)
- ⚪ **mensagem** (string): Mensagem personalizada (None se vazia)

### Validações Implementadas

#### 1. **Quantidade**
- Convertida para inteiro
- Valor mínimo: 0
- Valor padrão: 1 (se não enviado)

#### 2. **Mensagem**
- String vazia → armazenada como `None` no banco
- String preenchida → armazenada normalmente

#### 3. **Horário (HH:MM)**
- Regex: `^([01]?\d|2[0-3]):[0-5]\d$`
- Validação: 00:00 a 23:59
- Exemplo válido: `14:30`

#### 4. **Data (YYYY-MM-DD)**
- Formato: `YYYY-MM-DD`
- Validação com `datetime.strptime()`
- Exemplo: `2024-12-25`

### Resposta de Sucesso (Status 200)

```json
{
  "success": true,
  "pedido_id": 42,
  "message": "Pedido recebido e armazenado com sucesso",
  "dados_armazenados": {
    "cliente": "João Silva",
    "produto": "Buquê 12 rosas vermelhas",
    "quantidade": 1,
    "destinatario": "Maria Santos",
    "dia_entrega": "2024-12-25",
    "horario": "14:30",
    "status": "pendente"
  }
}
```

### Resposta de Erro (Status 400)

#### Campos Obrigatórios Ausentes
```json
{
  "error": "Campos obrigatórios ausentes: cliente, produto",
  "campos_enviados": ["destinatario", "mensagem"]
}
```

#### Formato de Horário Inválido
```json
{
  "error": "Formato de horário inválido",
  "horario_recebido": "25:99",
  "formato_esperado": "HH:MM (ex: 14:30)"
}
```

#### Formato de Data Inválido
```json
{
  "error": "Formato de data inválido",
  "data_recebida": "25-12-2024",
  "formato_esperado": "YYYY-MM-DD (ex: 2024-12-25)",
  "detalhes": "time data '25-12-2024' does not match format '%Y-%m-%d'"
}
```

#### Quantidade Inválida
```json
{
  "error": "Quantidade inválida: abc",
  "detalhes": "invalid literal for int() with base 10: 'abc'"
}
```

#### Erro no Banco de Dados (Status 500)
```json
{
  "error": "Erro ao inserir pedido no banco de dados",
  "detalhes": "UNIQUE constraint failed: pedidos.id"
}
```

---

## 📤 Código do PDFgen

### Função `enviar_pedido_para_painel`

```python
def enviar_pedido_para_painel(self, pedido: dict):
    """Envia pedido para o servidor Flask via POST"""
    try:
        import requests
        
        # Montar dados para envio conforme especificação da API
        dados_envio = {
            "cliente": pedido.get("cliente", ""),
            "produto": pedido.get("produto", ""),
            "quantidade": pedido.get("quantidade", 1),
            "horario": pedido.get("hora_entrega", ""),
            "dia_entrega": pedido.get("data_entrega", ""),
            "destinatario": pedido.get("destinatario", ""),
            "mensagem": pedido.get("mensagem", "")
        }
        
        # Enviar requisição POST para o servidor
        response = requests.post(
            "http://192.168.0.10:5000/api/pedidos",
            json=dados_envio,
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        
        # Verificar status da resposta
        response.raise_for_status()
        
        # Log de sucesso
        resposta_json = response.json()
        pedido_id = resposta_json.get('pedido_id', 'N/A')
        print(f"✅ Pedido #{pedido_id} enviado ao painel com sucesso!")
        
    except requests.exceptions.ConnectionError:
        print("⚠️ Erro de conexão: Servidor Flask não está acessível")
    except requests.exceptions.Timeout:
        print("⚠️ Timeout: O servidor não respondeu a tempo")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ Erro HTTP {e.response.status_code}: {e.response.text}")
    except Exception as e:
        print(f"⚠️ Erro ao enviar pedido ao painel: {e}")
```

### Estrutura do `pedido_record`

O dicionário `pedido_record` contém todos os dados do pedido:

```python
pedido_record = {
    'pedido_num': 42,
    'cliente': 'João Silva',
    'produto': 'Buquê 12 rosas vermelhas',
    'quantidade': 1,  # Valor padrão: 1
    'destinatario': 'Maria Santos',
    'mensagem': 'Feliz Aniversário!',
    'data_entrega': '2024-12-25',  # Convertido de DD/MM/YYYY para YYYY-MM-DD
    'hora_entrega': '14:30',  # Formato HH:MM
    'status': 'pendente'
}
```

---

## 🧪 Testes

### Teste com cURL

```bash
curl -X POST http://192.168.0.10:5000/api/pedidos \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "João Silva",
    "produto": "Buquê 12 rosas",
    "quantidade": 1,
    "horario": "14:30",
    "dia_entrega": "2024-12-25",
    "destinatario": "Maria Santos",
    "mensagem": "Feliz Aniversário!"
  }'
```

### Resposta Esperada

```json
{
  "success": true,
  "pedido_id": 42,
  "message": "Pedido recebido e armazenado com sucesso",
  "dados_armazenados": {
    "cliente": "João Silva",
    "produto": "Buquê 12 rosas",
    "quantidade": 1,
    "destinatario": "Maria Santos",
    "dia_entrega": "2024-12-25",
    "horario": "14:30",
    "status": "pendente"
  }
}
```

---

## ✅ Checklist de Funcionalidades

- ✅ Requisição POST do PDFgen ao Flask
- ✅ Envio de todos os dados necessários
- ✅ Validação de campos obrigatórios
- ✅ Conversão de quantidade para inteiro
- ✅ Mensagem vazia convertida para None
- ✅ Validação de formato HH:MM
- ✅ Validação de formato YYYY-MM-DD
- ✅ Inserção no banco de dados (SQLAlchemy)
- ✅ Resposta de sucesso (Status 200)
- ✅ Resposta de erro (Status 400)
- ✅ Tratamento de exceções completo
- ✅ Mensagens de erro descritivas
- ✅ Timeout configurado (5 segundos)
- ✅ Logs no PDFgen

---

## 🚀 Como Usar

### 1. Iniciar o Servidor Flask

```bash
cd Servidor\static
pip install -r requirements.txt
python app.py
```

O servidor estará em: `http://192.168.0.10:5000`

### 2. Executar o PDFgen

```bash
cd Clientes
pip install -r requirements.txt
python PDFgen.py
```

### 3. Fluxo Automático

1. Usuário preenche formulário no PDFgen
2. PDFgen gera o PDF
3. PDFgen envia POST para Flask
4. Flask valida e armazena
5. Flask responde com pedido_id
6. PDFgen exibe sucesso

---

## 🐛 Troubleshooting

### Erro: "Connection Refused"
**Causa:** Servidor Flask não está rodando
**Solução:** Execute `python app.py` na pasta `Servidor/static`

### Erro: "Timeout"
**Causa:** Servidor não responde em 5 segundos
**Solução:** Verifique a conexão de rede e se o servidor está acessível

### Erro: "Campos obrigatórios ausentes"
**Causa:** Dados não estão sendo enviados corretamente
**Solução:** Verifique se todos os campos estão no `pedido_record`

### Erro: "Formato de horário inválido"
**Causa:** Horário não está no formato HH:MM
**Solução:** Garanta que o horário esteja no formato correto (ex: 14:30)

### Erro: "Formato de data inválido"
**Causa:** Data não está no formato YYYY-MM-DD
**Solução:** Converta a data para o formato correto antes de enviar

---

## 📝 Notas Finais

- A integração é **assíncrona**: O PDF é gerado independentemente do envio ao servidor
- Se o envio falhar, o PDF ainda é salvo localmente
- O servidor valida todos os dados antes de inserir no banco
- As mensagens de erro são descritivas e úteis para debug

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

