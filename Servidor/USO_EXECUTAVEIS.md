# 🚀 Como Usar os Executáveis

## 📋 Dois Aplicativos Disponíveis

### 1. 📦 Gerador_De_Pedidos.exe

**Função:** Roda o servidor Flask e recebe pedidos via POST

**Uso:**
1. Execute `Gerador_De_Pedidos.exe`
2. Aguarde o servidor iniciar
3. Navegador abre automaticamente
4. O servidor reinicia automaticamente se cair

**Quando usar:**
- Quando quiser rodar o servidor manualmente
- Para processar pedidos do PDFgen
- Para desenvolvimento/testes
- Funciona 24/7 (não encerra)

**Características:**
- ✅ Inicia servidor Flask automaticamente
- ✅ Abre navegador automaticamente
- ✅ Mostra logs em tempo real
- ✅ Reinicia se o servidor cair
- ✅ Funciona continuamente

---

### 2. 🤖 Iniciar_Servidor.exe

**Função:** Inicia o servidor Flask automaticamente às 08:00

**Uso:**
1. Execute `Iniciar_Servidor.exe`
2. Se já são 08:00 ou depois → inicia imediatamente
3. Se ainda não são 08:00 → aguarda até 08:00
4. Servidor encerra automaticamente às 18:30
5. Reinicia na manhã seguinte

**Quando usar:**
- Para uso em produção
- Quando quer automação horária
- Para usar em computador da empresa
- Configurar no startup do Windows

**Características:**
- ✅ Inicia às 08:00 automaticamente
- ✅ Encerra às 18:30 automaticamente
- ✅ Inicia imediatamente se for após 08:00
- ✅ Reinicia se o servidor cair
- ✅ Monitora continuamente

---

## 🎯 Diferenças Entre os Apps

| Característica | Gerador_De_Pedidos.exe | Iniciar_Servidor.exe |
|----------------|------------------------|----------------------|
| Início | Imediato | Às 08:00 (ou imediatamente se após) |
| Encerramento | Manual (Ctrl+C) | Automático às 18:30 |
| Duração | 24/7 | 08:00 - 18:30 |
| Horário | Qualquer hora | Apenas horário comercial |
| Uso | Desenvolvimento/Teste | Produção/Automação |
| Monitoramento | Contínuo | Contínuo com horário |

---

## 📝 Como Compilar

### Passo 1: Instalar PyInstaller

```powershell
pip install pyinstaller
```

### Passo 2: Executar Script de Compilação

```powershell
cd Servidor
.\compilar.bat
```

### Passo 3: Encontrar os Executáveis

Os arquivos .exe estarão em:
```
Servidor/dist/Gerador_De_Pedidos.exe
Servidor/dist/Iniciar_Servidor.exe
```

---

## 🚀 Como Executar

### Teste Rápido: Gerador_De_Pedidos.exe

```powershell
cd Servidor\dist
.\Gerador_De_Pedidos.exe
```

**Resultado esperado:**
- Janela do terminal aberta
- Logs do servidor aparecem
- Navegador abre em http://localhost:5000
- Servidor fica rodando

### Teste Rápido: Iniciar_Servidor.exe

```powershell
cd Servidor\dist
.\Iniciar_Servidor.exe
```

**Se for antes das 08:00:**
- Mostra "Aguardando até 08:00"
- Aguarda até o horário
- Inicia automaticamente às 08:00

**Se for após 08:00:**
- Inicia imediatamente
- Mostra "Servidor iniciado com sucesso"
- Monitora continuamente

---

## ⚙️ Configurar no Windows Startup

### Opção 1: Pasta de Inicialização

1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Crie atalho para `Iniciar_Servidor.exe`

### Opção 2: Tarefa Agendada

1. Abra o **Agendador de Tarefas do Windows**
2. Clique em **Criar Tarefa Básica**
3. Nome: `Auto Iniciar Servidor`
4. Acionar: Quando o computador iniciar
5. Ação: Iniciar um programa
6. Programa: Caminho para `Iniciar_Servidor.exe`

---

## 🔧 Fluxo de Trabalho Completo

### Cenário 1: Desenvolvimento

```
1. Execute Gerador_De_Pedidos.exe
2. Servidor inicia imediatamente
3. Desenvolvimento/testes
4. Encerre quando terminar (Ctrl+C)
```

### Cenário 2: Produção

```
1. Execute Iniciar_Servidor.exe na manhã
2. Servidor inicia às 08:00
3. Funciona durante o dia
4. Encerra às 18:30 automaticamente
5. Na manhã seguinte, inicia novamente às 08:00
```

### Cenário 3: 24/7

```
1. Execute Gerador_De_Pedidos.exe
2. Deixe rodando continuamente
3. Servidor reinicia automaticamente se cair
4. Nunca encerra (a menos que feche manualmente)
```

---

## 🐛 Troubleshooting

### Executável não inicia

**Causa:** Python não encontrado
**Solução:** Use `--onefile` no PyInstaller

### Servidor não conecta

**Verifique:**
1. Firewall não está bloqueando porta 5000
2. IP está correto (192.168.1.148)
3. PDFgen está configurado corretamente

### Executável fecha imediatamente

**Causa:** Erro ao iniciar servidor Flask
**Solução:** Veja os logs no terminal ao executar

---

## 📊 Monitoramento

### Logs do Gerador_De_Pedidos.exe

```
[08:00:00] 🚀 Iniciando servidor Flask...
[08:00:03] ✅ Servidor Flask iniciado com sucesso!
[08:00:03] 📋 PID do processo: 12345
[08:00:03] 🌐 URL: http://localhost:5000
[08:00:03] 🔄 Monitoramento ativo...
[08:05:00] ⚠️ Servidor Flask encerrou (código: -1)
[08:05:01] 🔄 Reiniciando servidor...
```

### Logs do Iniciar_Servidor.exe

```
[07:50:00] ⏳ Aguardando até 08:00...
[07:50:00]    Horário atual: 07:50
[08:00:00] ✓ Horário 08:00 alcançado!
[08:00:00] 🚀 Iniciando servidor Flask...
[08:00:03] ✅ Servidor Flask iniciado com sucesso!
[18:30:00] ⏰ Horário de encerramento alcançado
[18:30:00] 🛑 Parando servidor...
```

---

## ✅ Checklist de Uso

### Antes de Usar:
- [ ] Executáveis compilados
- [ ] Servidor/static/app.py existe
- [ ] Dependências instaladas

### Ao Usar Gerador_De_Pedidos.exe:
- [ ] Executável iniciou
- [ ] Servidor está acessível
- [ ] PDFgen consegue enviar pedidos
- [ ] Logs aparecem na tela

### Ao Usar Iniciar_Servidor.exe:
- [ ] Executável iniciou
- [ ] Aguardando horário correto (se antes de 08:00)
- [ ] Servidor inicia automaticamente
- [ ] Encerra às 18:30

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

