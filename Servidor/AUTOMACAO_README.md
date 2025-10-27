# 🤖 Automação do Servidor Flask

## 📋 Visão Geral

O script `iniciar_automático.py` automatiza a inicialização e monitoramento do servidor Flask:

- ✅ Inicia automaticamente às **08:00**
- ✅ Encerra automaticamente às **18:30**
- ✅ Reinicia automaticamente se o servidor cair
- ✅ Monitora o status a cada 60 segundos
- ✅ Compatível com Windows e Linux/Mac

---

## 🚀 Como Usar

### Windows (PowerShell)

```powershell
cd Servidor
.\iniciar_automático.ps1
```

### Windows (CMD)

```cmd
cd Servidor
iniciar_automático.bat
```

### Linux/Mac

```bash
cd Servidor
python iniciar_automático.py
```

---

## ⚙️ Configurações

As configurações podem ser alteradas no início do arquivo `iniciar_automático.py`:

```python
HORA_INICIO = dt_time(8, 0)      # 08:00
HORA_FIM = dt_time(18, 30)       # 18:30
CHECK_INTERVAL = 60               # Verificar a cada 60 segundos
FLASK_SCRIPT = "app.py"           # Nome do arquivo Flask
DIRETORIO = "static"              # Diretório onde está o app.py
```

---

## 🔄 Fluxo de Funcionamento

```
1. Script inicia
   ↓
2. Verifica horário atual
   ↓
3. Se horário ≥ 08:00
   → Inicia servidor Flask imediatamente
   ↓
4. Entra em loop de monitoramento
   ↓
5. A cada 60 segundos:
   - Verifica se servidor está rodando
   - Verifica se horário permite execução
   ↓
6. Se servidor caiu e horário OK:
   → Reinicia automaticamente
   ↓
7. Se horário ≥ 18:30:
   → Encerra servidor automaticamente
   ↓
8. Volta ao passo 5
```

---

## 📊 Funcionalidades

### Início Automático

O script verifica o horário:
- **Se já são 08:00 ou depois:** Inicia o servidor imediatamente
- **Se ainda não são 08:00:** Aguarda até 08:00 para iniciar

### Monitoramento Contínuo

O script monitora:
- Status do servidor Flask (rodando/caiu)
- Horário atual (dentro/fora do horário de funcionamento)
- Processo do servidor

### Reinício Automático

Se o servidor Flask cair ou encerrar acidentalmente:
- Script detecta o encerramento
- Reinicia automaticamente (se dentro do horário)
- Mantém o servidor sempre disponível

### Encerramento Automático

Às **18:30**:
- Servidor é encerrado automaticamente
- Script continua monitorando
- Na manhã seguinte (08:00), inicia novamente

---

## 🛑 Como Parar

### Parar Temporariamente

No terminal, pressione: `Ctrl+C`

Isso irá:
1. Parar o servidor Flask
2. Encerrar o script de automação

### Parar Permanentemente

Encerre a janela do terminal ou feche o script.

---

## 🔧 Manutenção

### Verificar Logs

O script exibe logs em tempo real:
```
[2024-12-20 08:00:00] 🚀 Iniciando servidor Flask...
[2024-12-20 08:00:03] ✅ Servidor Flask iniciado com sucesso!
[2024-12-20 08:00:03]    PID: 12345
[2024-12-20 08:05:00] ⏰ Próxima verificação em 60 segundos...
```

### Reiniciar o Servidor Manualmente

Se precisar reiniciar o servidor manualmente:
1. Pressione `Ctrl+C` para parar o script
2. Execute o script novamente

---

## 🎯 Iniciar com Windows

### Opção 1: Tarefa Agendada

1. Abra o **Agendador de Tarefas do Windows**
2. Clique em **Criar Tarefa Básica**
3. Nome: `Auto Flask Server`
4. Acionar: Quando eu fizer login
5. Ação: Iniciar um programa
6. Programa: `powershell.exe`
7. Argumentos: `-File "C:\caminho\para\Servidor\iniciar_automático.ps1"`

### Opção 2: Pasta de Inicialização

1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Crie um atalho para `iniciar_automático.bat` ou `iniciar_automático.ps1`

---

## 🐛 Troubleshooting

### Erro: "Python não encontrado"
**Solução:** Instale Python e adicione ao PATH

### Erro: "app.py não encontrado"
**Solução:** Execute o script da pasta `Servidor/`

### Servidor não inicia
**Verifique:**
1. Dependências instaladas: `pip install -r static/requirements.txt`
2. Porta 5000 disponível
3. Sem outro processo usando a porta

### Servidor reinicia constantemente
**Causa:** Erro no servidor Flask
**Solução:** Verifique os logs do Flask em `static/app.py`

---

## 📝 Exemplo de Uso

### Cenário 1: Iniciar às 07:50

```bash
python iniciar_automático.py
```

**Output:**
```
[2024-12-20 07:50:00] ⏳ Aguardando até 08:00...
[2024-12-20 07:50:00]    Horário atual: 07:50
[2024-12-20 07:51:00] ⏰ Próxima verificação em 60 segundos...
[2024-12-20 08:00:00] ✓ Horário 08:00 alcançado!
[2024-12-20 08:00:00] 🚀 Iniciando servidor Flask...
[2024-12-20 08:00:03] ✅ Servidor Flask iniciado com sucesso!
```

### Cenário 2: Iniciar às 09:00

```bash
python iniciar_automático.py
```

**Output:**
```
[2024-12-20 09:00:00] ✓ Horário já é 09:00 - servidor pode iniciar
[2024-12-20 09:00:00] 🚀 Iniciando servidor Flask...
[2024-12-20 09:00:03] ✅ Servidor Flask iniciado com sucesso!
```

### Cenário 3: Servidor Cai (Reinício Automático)

```bash
# Servidor em execução
[2024-12-20 10:30:00] 🔄 Loop de monitoramento...

# Servidor cai (erro, fechamento, etc.)
[2024-12-20 10:31:00] ⚠️ Servidor Flask encerrou (exit code: -1)
[2024-12-20 10:31:00] 🔄 Servidor não está rodando, reiniciando...
[2024-12-20 10:31:00] 🚀 Iniciando servidor Flask...
[2024-12-20 10:31:03] ✅ Servidor Flask iniciado com sucesso!
```

### Cenário 4: Encerramento Automático

```bash
# Servidor em execução
[2024-12-20 18:29:00] 🔄 Loop de monitoramento...

# Chegou às 18:30
[2024-12-20 18:30:00] ⏰ Horário de encerramento alcançado, parando servidor...
[2024-12-20 18:30:00] 🛑 Parando servidor Flask...
[2024-12-20 18:30:00] ✅ Servidor Flask encerrado
```

---

## ✅ Checklist

- [x] Script de automação criado
- [x] Início automático às 08:00
- [x] Encerramento automático às 18:30
- [x] Reinício automático se servidor cair
- [x] Monitoramento a cada 60 segundos
- [x] Compatível Windows e Linux
- [x] Scripts .bat e .ps1 criados
- [x] Documentação completa

---

## 📝 Notas Finais

- O servidor Flask será acessível em: `http://localhost:5000`
- Em rede: `http://192.168.1.148:5000`
- O script mantém o servidor sempre disponível durante o horário de funcionamento
- Mantenha o script rodando em background para máxima eficiência

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

