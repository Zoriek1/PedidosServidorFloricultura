# 🚀 Instruções para Iniciar o Servidor

## Passo 1: Instalar Dependências

Abra o PowerShell ou Terminal e execute:

```powershell
cd Servidor\static
pip install -r requirements.txt
```

## Passo 2: Executar o Servidor

```powershell
python app.py
```

O servidor será iniciado em: **http://localhost:5000**

## Passo 3: Acessar no Navegador

Abra o navegador e acesse:
- **Local:** http://localhost:5000
- **Rede:** http://192.168.0.10:5000

## ✅ Pronto!

Agora você pode:
1. ✅ Criar novos pedidos através do formulário
2. ✅ Visualizar todos os pedidos no painel
3. ✅ Atualizar o status dos pedidos
4. ✅ Deletar pedidos
5. ✅ Receber pedidos da aplicação desktop

---

## 📋 Funcionalidades Implementadas

### Rotas Web
- ✅ `GET /` - Listagem de pedidos
- ✅ `GET /criar-pedido` - Formulário de criação
- ✅ `POST /criar-pedido` - Processar formulário
- ✅ `POST /pedido/<id>/atualizar-status` - Atualizar status
- ✅ `POST /pedido/<id>/deletar` - Deletar pedido

### API REST
- ✅ `POST /api/pedidos` - Criar pedido via JSON

### Validações
- ✅ Conversão de quantidade para inteiro (mínimo 0)
- ✅ Mensagem vazia → None no banco
- ✅ Formato de data: YYYY-MM-DD
- ✅ Formato de horário: HH:MM
- ✅ Campos obrigatórios validados

---

## 🔧 Configuração de Rede

Para acessar de outras máquinas na mesma rede, certifique-se de:

1. O servidor já está configurado com `host='0.0.0.0'` ✅
2. Use o IP local da sua máquina (ex: `http://192.168.0.10:5000`)
3. Verifique se o firewall permite conexões na porta 5000

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução:** Instale as dependências:
```powershell
pip install -r requirements.txt
```

### Erro: "Address already in use"
**Solução:** Altere a porta no arquivo `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Banco de dados não é criado
**Solução:** Verifique permissões de escrita na pasta `static/`

---

## 📝 Próximos Passos

1. Execute o servidor com `python app.py`
2. Abra http://localhost:5000 no navegador
3. Teste criando um pedido
4. A aplicação desktop se conectará automaticamente ao servidor

---

**Desenvolvido para Plante Uma Flor Floricultura** 🌺

