# 🔧 Scripts de Gerenciamento do Servidor HTTPS

## 📋 Scripts Disponíveis

### 🚀 Iniciar Servidor

#### `iniciar_servidor_https_invisivel.vbs`
**Inicia o servidor HTTPS em background (sem janela de comando)**

- ✅ Servidor roda invisível
- ✅ Configura encoding UTF-8 automaticamente
- ✅ Gera arquivo de log: `backend/servidor_https.log`
- ✅ Mostra notificação quando inicia

**Como usar:**
- Duplo clique no arquivo
- Ou pelo Explorador: clique com direito → Abrir

**Vantagens:**
- Não fica janela de comando aberta
- Pode minimizar tudo e o servidor continua rodando
- Pode ser configurado para iniciar com o Windows

---

### 🛑 Parar Servidor

#### `parar_servidor_https.bat`
**Para o servidor HTTPS que está rodando em background**

- Mata processos Python na porta 5000
- Mata processos rodando `main.py --https`
- Verifica se parou corretamente

**Como usar:**
```batch
parar_servidor_https.bat
```

---

### 🔍 Verificar Status

#### `verificar_servidor_https.bat`
**Verifica se o servidor está rodando e mostra o log**

- Mostra se o servidor está ativo
- Exibe o PID do processo
- Mostra as últimas 20 linhas do log

**Como usar:**
```batch
verificar_servidor_https.bat
```

**Útil para:**
- Ver se o servidor iniciou corretamente
- Debug de erros
- Verificar mensagens de log

---

## 📝 Arquivo de Log

Quando o servidor roda via VBS, todas as mensagens são salvas em:

```
backend\servidor_https.log
```

**O log contém:**
- ✅ Mensagens de inicialização
- ✅ Erros (se houver)
- ✅ Requisições HTTP
- ✅ Status do banco de dados

**Para ver o log em tempo real:**
```batch
type backend\servidor_https.log
```

Ou abra o arquivo em um editor de texto.

---

## 🔧 Solução de Problemas

### Servidor não inicia

1. **Verifique o log:**
   ```batch
   verificar_servidor_https.bat
   ```

2. **Procure por erros** no arquivo `servidor_https.log`

3. **Certificados faltando?**
   - Execute: `backend\ssl\GERAR_CERTIFICADOS_AUTO.bat`

4. **Porta 5000 ocupada?**
   - Pare outros servidores
   - Ou mude a porta em `config_servidor.ini`

### Servidor não para

1. **Tente o script de parar:**
   ```batch
   parar_servidor_https.bat
   ```

2. **Se não funcionar, force:**
   ```batch
   parar_servidor_forcado.bat
   ```

3. **Manual (último recurso):**
   - Ctrl+Alt+Del → Gerenciador de Tarefas
   - Procure por "python.exe"
   - Finalize o processo

### Quero ver o que está acontecendo

**Opção 1:** Rode com janela visível
```batch
cd backend
python main.py --https
```

**Opção 2:** Monitore o log
```batch
powershell -Command "Get-Content backend\servidor_https.log -Wait"
```

---

## 🎯 Fluxo de Uso Recomendado

### Primeira vez:

1. **Configure certificados:**
   ```batch
   backend\CONFIGURAR_SERVIDOR.bat
   ```

2. **Inicie o servidor:**
   - Duplo clique em `iniciar_servidor_https_invisivel.vbs`

3. **Verifique se iniciou:**
   ```batch
   verificar_servidor_https.bat
   ```

4. **Acesse:** `https://192.168.1.148:5000`

### Uso diário:

1. **Iniciar:** Duplo clique em `iniciar_servidor_https_invisivel.vbs`
2. **Usar:** Acesse `https://192.168.1.148:5000`
3. **Parar:** Execute `parar_servidor_https.bat`

### Debug:

1. **Ver status:** `verificar_servidor_https.bat`
2. **Ver log completo:** Abra `backend\servidor_https.log`
3. **Rodar com janela:** `python main.py --https` (no terminal)

---

## 🔄 Inicialização Automática

Para o servidor iniciar automaticamente com o Windows:

1. **Pressione `Win + R`**
2. **Digite:** `shell:startup`
3. **Crie atalho** de `iniciar_servidor_https_invisivel.vbs` nessa pasta

Pronto! O servidor iniciará automaticamente ao ligar o PC.

---

## 📊 Comparação de Métodos

| Método | Janela | Log | Auto-start | Debug |
|--------|--------|-----|-----------|-------|
| VBS (invisível) | ❌ Não | ✅ Arquivo | ✅ Sim | ⚠️ Médio |
| BAT (visível) | ✅ Sim | ✅ Console | ❌ Não | ✅ Fácil |
| Terminal | ✅ Sim | ✅ Console | ❌ Não | ✅ Muito fácil |

**Recomendação:**
- **Uso normal:** VBS invisível
- **Debug/Testes:** Terminal ou BAT
- **Produção:** VBS + Auto-start

---

## 🆘 Scripts de Emergência

Se nada funcionar:

```batch
# Matar TUDO relacionado a Python
taskkill /F /IM python.exe

# Limpar porta 5000
netstat -ano | findstr :5000
# Anote o PID e:
taskkill /F /PID [PID]
```

---

**Última atualização:** Outubro 2025
**Versão:** 1.0

