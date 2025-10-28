# ✅ Solução do Erro de Conexão

## 🔍 Problema Identificado

Você recebeu o erro:
```
⚠️ Erro de conexão: Servidor Flask não está acessível em http://192.168.0.10:5000
```

### Causas:
1. ❌ Servidor Flask não está rodando
2. ❌ IP incorreto (era `192.168.0.10`, corrigido para `192.168.1.148`)

---

## ✅ Correções Aplicadas

### 1. IP Atualizado
O IP foi atualizado no arquivo `Clientes/PDFgen.py` (linha 934):

**Antes:**
```python
"http://192.168.0.10:5000/api/pedidos"
```

**Depois:**
```python
"http://192.168.1.148:5000/api/pedidos"
```

### 2. Scripts Criados
Foram criados scripts para facilitar o início do servidor:
- `Servidor/iniciar_servidor.ps1` (PowerShell)
- `Servidor/iniciar_servidor.bat` (CMD)

### 3. Script de Teste
Criado `testar_conexao.py` para testar a conexão

---

## 🚀 Como Resolver

### Passo 1: Iniciar o Servidor Flask

**Opção A - Usando PowerShell (Recomendado):**
```powershell
cd Servidor
.\iniciar_servidor.ps1
```

**Opção B - Manualmente:**
```powershell
cd Servidor\static
python app.py
```

### Passo 2: Verificar se o Servidor Está Rodando

Você deve ver no terminal:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.148:5000
```

Acesse no navegador:
- http://localhost:5000

### Passo 3: Testar a Conexão

Execute o script de teste:
```powershell
python testar_conexao.py
```

Se tudo estiver correto, você verá:
```
✅ SUCESSO! Pedido enviado com sucesso!
📋 ID do Pedido: 1
💬 Mensagem: Pedido recebido e armazenado com sucesso
```

### Passo 4: Executar o PDFgen

```powershell
cd Clientes
python PDFgen.py
```

Agora deve funcionar sem erros! ✅

---

## 🎯 Verificação Rápida

Execute este comando para verificar se o servidor está rodando:

```powershell
# Teste 1: Verificar se o servidor responde
curl http://192.168.1.148:5000

# Teste 2: Verificar se a API funciona
python testar_conexao.py
```

---

## 📋 Checklist

- [x] IP atualizado no PDFgen
- [x] Scripts de início criados
- [x] Script de teste criado
- [ ] Servidor Flask rodando
- [ ] Teste de conexão bem-sucedido
- [ ] PDFgen funcionando

---

## 🔧 Se o Erro Persistir

### Erro: "Connection Refused"
**Causa:** Servidor não está rodando
**Solução:** Execute `cd Servidor` e `.\iniciar_servidor.ps1`

### Erro: "Timeout"
**Causa:** Firewall bloqueando
**Solução:** Permita a porta 5000 no firewall do Windows

### Erro: "ModuleNotFoundError"
**Causa:** Dependências não instaladas
**Solução:** Execute `pip install -r Servidor/static/requirements.txt`

---

## 📝 Notas Importantes

1. O servidor deve estar rodando ANTES de executar o PDFgen
2. Mantenha o servidor ativo enquanto usa o PDFgen
3. Para parar o servidor, pressione `Ctrl+C`
4. O IP pode mudar (especialmente com WiFi). Se isso acontecer, execute:
   ```powershell
   ipconfig | Select-String -Pattern "IPv4"
   ```
   E atualize o IP no arquivo `Clientes/PDFgen.py` linha 934

---

## 🎉 Resultado Esperado

Quando tudo estiver correto:

1. Servidor Flask rodando em background
2. PDFgen executado
3. Um pedido criado no PDFgen
4. No console do PDFgen você verá:
   ```
   ✅ Pedido #1 enviado ao painel com sucesso!
   ```
5. No navegador (http://localhost:5000), o pedido aparece na listagem

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

