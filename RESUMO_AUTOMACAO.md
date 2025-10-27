# 🤖 Resumo da Automação - Servidor Flask

## ✅ O Que Foi Implementado

### Script de Automação Completo

Foi criado o script `iniciar_automático.py` que:

1. ✅ **Inicia automaticamente às 08:00**
   - Se o PC for ligado após 08:00, inicia imediatamente
   - Se ainda não são 08:00, aguarda até esse horário

2. ✅ **Encerra automaticamente às 18:30**
   - Servidor é encerrado automaticamente
   - Script continua monitorando

3. ✅ **Reinicia automaticamente se o servidor cair**
   - Monitora o status do servidor Flask a cada 60 segundos
   - Se o servidor encerrar, reinicia automaticamente
   - Garante disponibilidade contínua

4. ✅ **Monitores contínuos**
   - Verifica horário atual
   - Verifica status do servidor
   - Toma ações automáticas

5. ✅ **Compatível Windows e Linux**
   - Usa subprocess para rodar o Flask em background
   - Tratamento de sinais adequado para cada OS

---

## 📁 Arquivos Criados

### 1. `Servidor/iniciar_automático.py`
Script principal de automação (Python)

### 2. `Servidor/iniciar_automático.bat`
Script de inicialização para Windows (CMD)

### 3. `Servidor/iniciar_automático.ps1`
Script de inicialização para Windows (PowerShell)

### 4. `Servidor/AUTOMACAO_README.md`
Documentação completa da automação

---

## 🚀 Como Usar

### Windows (Recomendado)

**PowerShell:**
```powershell
cd Servidor
.\iniciar_automático.ps1
```

**CMD:**
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

### Configuração Padrão

```python
HORA_INICIO = 08:00      # Início automático
HORA_FIM = 18:30         # Encerramento automático
CHECK_INTERVAL = 60      # Verificar a cada 60 segundos
```

### Personalizar Configurações

Edite o arquivo `Servidor/iniciar_automático.py`:

```python
# Mudar horário de início para 07:00
HORA_INICIO = dt_time(7, 0)

# Mudar horário de encerramento para 19:00
HORA_FIM = dt_time(19, 0)

# Mudar intervalo de verificação para 30 segundos
CHECK_INTERVAL = 30
```

---

## 🔄 Fluxo de Funcionamento

### 1. Início

```
Script inicia
   ↓
Verifica horário atual
   ↓
Se horário ≥ 08:00:
   → Inicia servidor Flask IMEDIATAMENTE
   ↓
Se horário < 08:00:
   → Aguarda até 08:00
```

### 2. Monitoramento Contínuo

```
Loop a cada 60 segundos:
   ↓
1. Verifica se servidor está rodando
   ↓
2. Verifica se horário permite execução
   ↓
3. Se servidor caiu E horário OK:
   → Reinicia servidor
   ↓
4. Se horário ≥ 18:30:
   → Encerra servidor
   ↓
5. Volta ao início do loop
```

### 3. Encerramento

```
Horário ≥ 18:30
   ↓
Servidor Flask encerrado
   ↓
Script continua monitorando
   ↓
Na manhã seguinte (08:00):
   → Inicia novamente
```

---

## 🎯 Exemplos de Uso

### Cenário 1: Ligar o PC às 07:30

```bash
python iniciar_automático.py
```

**Resultado:**
- Script inicia
- Aguarda até 08:00
- Inicia servidor Flask às 08:00
- Monitora continuamente

### Cenário 2: Ligar o PC às 10:00

```bash
python iniciar_automático.py
```

**Resultado:**
- Script inicia
- Verifica: já são 10:00
- Inicia servidor Flask IMEDIATAMENTE
- Monitora continuamente

### Cenário 3: Servidor Cai (10:30)

**Situação:** Servidor Flask encerra acidentalmente

**Resultado:**
- Script detecta encerramento (próximo check)
- Verifica horário (10:30 - OK)
- Reinicia servidor automaticamente
- Continua funcionando normalmente

### Cenário 4: Fim do Dia (18:30)

**Resultado:**
- Script detecta horário (18:30)
- Encerra servidor Flask automaticamente
- Script continua monitorando
- Server fica desligado até 08:00 do dia seguinte

---

## 🛑 Como Parar

### Parar Manualmente

No terminal, pressione: `Ctrl+C`

### Configurar para Parar Automaticamente

O servidor encerra automaticamente às **18:30**.

---

## 📊 Logs do Script

### Exemplo de Execução

```
============================================================
🌺 Automação do Servidor Flask - Plante Uma Flor
============================================================

[2024-12-20 08:00:00] 📅 Início automático: 08:00
[2024-12-20 08:00:00] 📅 Encerramento automático: 18:30
[2024-12-20 08:00:00] 🔄 Intervalo de verificação: 60 segundos

[2024-12-20 08:00:00] 🚀 Iniciando servidor Flask...
[2024-12-20 08:00:03] ✅ Servidor Flask iniciado com sucesso!
[2024-12-20 08:00:03]    PID: 12345
[2024-12-20 08:01:00] 🔄 Iniciando loop de monitoramento...
[2024-12-20 08:01:00]    Pressione Ctrl+C para parar o script e o servidor

[2024-12-20 08:02:00] ⏰ Próxima verificação em 60 segundos...
[2024-12-20 08:03:00] ⏰ Próxima verificação em 60 segundos...
...
[2024-12-20 18:29:00] ⏰ Próxima verificação em 60 segundos...
[2024-12-20 18:30:00] ⏰ Horário de encerramento alcançado, parando servidor...
[2024-12-20 18:30:00] 🛑 Parando servidor Flask...
[2024-12-20 18:30:00] ✅ Servidor Flask encerrado
[2024-12-20 18:31:00] ⏰ Próxima verificação em 60 segundos...
```

### Exemplo de Reinício Automático

```
[2024-12-20 10:30:00] ⏰ Próxima verificação em 60 segundos...
[2024-12-20 10:31:00] ⚠️ Servidor Flask encerrou (exit code: -1)
[2024-12-20 10:31:00] 🔄 Servidor não está rodando, reiniciando...
[2024-12-20 10:31:00] 🚀 Iniciando servidor Flask...
[2024-12-20 10:31:03] ✅ Servidor Flask iniciado com sucesso!
[2024-12-20 10:31:03]    PID: 12346
[2024-12-20 10:32:00] ⏰ Próxima verificação em 60 segundos...
```

---

## 🔧 Melhorias Futuras

Possíveis melhorias que podem ser implementadas:

### 1. Email de Notificação
- Enviar email quando servidor cair
- Notificar início/encerramento do servidor

### 2. Log em Arquivo
- Salvar logs em arquivo de texto
- Histórico de reinícios

### 3. Interface Web
- Dashboard para ver status do servidor
- Controle via web

### 4. Múltiplos Servidores
- Iniciar vários servidores simultaneamente
- Balanceamento de carga

---

## ✅ Checklist Final

- [x] Script de automação criado
- [x] Início automático às 08:00
- [x] Encerramento automático às 18:30
- [x] Reinício automático se servidor cair
- [x] Monitoramento contínuo (60 segundos)
- [x] Compatível Windows e Linux
- [x] Scripts .bat e .ps1 criados
- [x] Documentação completa
- [x] Tratamento de erros
- [x] Logs informativos

---

## 📝 Notas Importantes

1. **Mantenha o script rodando:** O script deve ficar em execução durante o horário de funcionamento

2. **Não feche a janela:** Fechar a janela do script encerra o servidor Flask

3. **Permissões:** Certifique-se de que o Python tem permissões para criar processos

4. **Firewall:** Certifique-se de que a porta 5000 está aberta no firewall

5. **Dependências:** Execute `pip install -r static/requirements.txt` antes de usar

---

**Status:** 🟢 PRONTO PARA PRODUÇÃO

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

