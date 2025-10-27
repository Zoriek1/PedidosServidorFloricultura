# 🚀 Como Iniciar o Servidor Flask

## ⚠️ Problema Identificado

Você recebeu o erro:
```
⚠️ Erro de conexão: Servidor Flask não está acessível em http://192.168.0.10:5000
```

**Causa:** O servidor Flask não está rodando.

---

## ✅ Solução: Iniciar o Servidor

### Opção 1: Usando o Script (Mais Fácil)

**Windows (PowerShell):**
```powershell
cd Servidor
.\iniciar_servidor.ps1
```

**Windows (CMD/Batch):**
```cmd
cd Servidor
iniciar_servidor.bat
```

### Opção 2: Manualmente

**Passo 1:** Abra um terminal e navegue até a pasta do servidor:
```powershell
cd Servidor\static
```

**Passo 2:** Instale as dependências (se ainda não fez):
```powershell
pip install -r requirements.txt
```

**Passo 3:** Inicie o servidor:
```powershell
python app.py
```

---

## 🎯 Verificação

### Se o servidor estiver rodando, você verá:

```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.148:5000
```

### Acesse no navegador:
- **Local:** http://localhost:5000
- **Rede:** http://192.168.1.148:5000

---

## 🔧 Configuração de IP

O **PDFgen** está configurado para enviar pedidos para:
```
http://192.168.1.148:5000/api/pedidos
```

Se o IP da sua máquina mudar, você precisa atualizar o arquivo `Clientes/PDFgen.py` na linha 934:

```python
response = requests.post(
    "http://SEU_IP_AQUI:5000/api/pedidos",
    json=dados_envio,
    timeout=5
)
```

### Para descobrir seu IP:
```powershell
ipconfig | Select-String -Pattern "IPv4"
```

---

## 📋 Checklist

- [ ] Servidor Flask rodando
- [ ] Servidor acessível em http://localhost:5000
- [ ] IP correto configurado no PDFgen
- [ ] Dependências instaladas (Flask, SQLAlchemy)

---

## 🔍 Troubleshooting

### Erro: "python não é reconhecido"
**Solução:** Instale Python 3.7+ de https://www.python.org

### Erro: "pip não é reconhecido"
**Solução:** Adicione Python ao PATH durante a instalação

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução:** Execute `pip install -r requirements.txt`

### Erro: "Address already in use"
**Solução:** Altere a porta no arquivo `app.py` linha 244:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

E atualize o IP no PDFgen para usar `5001` ao invés de `5000`.

### Servidor roda mas o PDFgen não conecta
**Verifique:**
1. Firewall não está bloqueando a porta 5000
2. IP está correto no PDFgen
3. Servidor está acessível: abra http://192.168.1.148:5000 no navegador

---

## 🎯 Fluxo de Teste

1. **Inicie o servidor:**
   ```powershell
   cd Servidor
   .\iniciar_servidor.ps1
   ```

2. **Abra o navegador em:** http://localhost:5000

3. **Execute o PDFgen:**
   ```powershell
   cd Clientes
   python PDFgen.py
   ```

4. **Crie um pedido no PDFgen**

5. **Verifique o console do servidor** - deve mostrar a requisição POST

6. **Verifique o painel web** - o pedido deve aparecer

---

## 📝 Notas

- O servidor deve estar rodando ANTES de executar o PDFgen
- Mantenha o servidor ativo enquanto usa o PDFgen
- Para parar o servidor, pressione `Ctrl+C` no terminal

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

