# 🔨 Build do PDFgen.exe - Guia Completo

## ✨ Novidades v2.0

- 🌐 **Descoberta Automática de Rede** via UDP Broadcast
- 🔄 **Fallback Inteligente** para IPs comuns
- 📡 **Integração completa** com painel web v2.0
- 🎯 **Zero configuração** de IP necessária

## 🚀 Compilação Rápida

### Opção 1: Automática (Recomendada)

```bash
COMPILAR.bat
```

Isso vai:
1. ✅ Verificar PyInstaller
2. ✅ Instalar dependências
3. ✅ Limpar builds antigos
4. ✅ Compilar PDFgen.exe
5. ✅ Criar executável em `dist/PDFgen.exe`

### Opção 2: Manual

```bash
# 1. Instalar dependências
pip install -r requirements.txt
pip install pyinstaller

# 2. Compilar
pyinstaller PDFgen.spec --clean --noconfirm

# 3. Executável estará em dist/PDFgen.exe
```

## 🧪 Testar Antes de Compilar

Execute o teste de descoberta de rede:

```bash
python TESTAR_DISCOVERY.py
```

Isso vai:
- 🔍 Procurar servidor via broadcast UDP
- 🔄 Tentar fallback com IPs comuns
- 📊 Testar API do servidor
- ✅ Confirmar se está tudo OK

## 📋 Requisitos

- Python 3.8+
- PyInstaller 5.0+
- reportlab
- requests

## 📁 Estrutura de Build

```
Clientes/
├── PDFgen.py              # Código fonte (com descoberta de rede)
├── PDFgen.spec            # Configuração PyInstaller
├── COMPILAR.bat           # Script de compilação automática
├── TESTAR_DISCOVERY.py    # Script de teste
├── requirements.txt       # Dependências
├── *.ttf                  # Fontes (incluídas no .exe)
├── Buques.ico             # Ícone
│
├── build/                 # Arquivos temporários (pode deletar)
└── dist/
    └── PDFgen.exe         # ⭐ EXECUTÁVEL FINAL
```

## 🌐 Como Funciona a Descoberta Automática

### 1. Broadcast UDP (Método Principal)
```
Cliente escuta porta 37020 (UDP)
↓
Servidor envia broadcasts a cada 5s
↓
Cliente detecta e extrai IP+porta
↓
Conecta automaticamente!
```

### 2. Fallback Inteligente
Se broadcast falhar, tenta IPs comuns:
- 192.168.1.148 (IP atual conhecido)
- 192.168.1.100
- 192.168.1.101
- 192.168.0.100
- localhost
- Mais...

### 3. Cache de Sessão
- Descobre uma vez por sessão
- Reutiliza URL encontrada
- Performance otimizada

## ✅ Checklist de Compilação

- [ ] Dependências instaladas (`pip install -r requirements.txt pyinstaller`)
- [ ] Servidor rodando (para testar)
- [ ] Teste de descoberta OK (`python TESTAR_DISCOVERY.py`)
- [ ] Arquivos de fonte (.ttf) na pasta
- [ ] Ícone (Buques.ico) presente
- [ ] Compilação executada (`COMPILAR.bat`)
- [ ] Executável testado em máquina limpa
- [ ] Descoberta automática funcionando

## 🎯 Testar o Executável

### Em Máquina com Python
```bash
cd dist
PDFgen.exe
```

### Em Máquina Limpa (sem Python)
1. Copie `dist/PDFgen.exe` para outra máquina
2. Execute normalmente
3. Deve encontrar servidor automaticamente!
4. ✅ Sem configuração de IP necessária!

## 📊 Logs de Conexão

O PDFgen.exe mostra no console:
```
🔍 Procurando servidor na rede...
✅ Servidor encontrado via broadcast: http://192.168.1.148:5000
📤 Enviando pedido para: http://192.168.1.148:5000/api/pedidos
✅ Pedido #123 enviado ao painel v2.0 com sucesso!
```

## 🐛 Troubleshooting

### Erro: "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "Servidor não encontrado"
1. Verifique se servidor está rodando
2. Execute: `python TESTAR_DISCOVERY.py`
3. Verifique firewall (portas 5000 TCP e 37020 UDP)
4. Confirme mesma rede

### Executável não encontra servidor
1. Firewall bloqueando?
2. Mesma rede local?
3. Servidor rodando?
4. Teste direto: `curl http://localhost:5000/api/stats`

### Fontes não aparecem no PDF
- Verifique se os .ttf estão na pasta Clientes/
- Confirme que estão no PDFgen.spec (seção `datas`)
- Recompile com `--clean`

## 📦 Distribuição

Para distribuir:
1. Copie apenas `dist/PDFgen.exe`
2. **Não precisa** de Python instalado
3. **Não precisa** configurar IP
4. **Funciona** automaticamente na rede!

## 🎉 Pronto!

Seu PDFgen.exe está pronto com:
- ✅ Descoberta automática de servidor
- ✅ Integração com painel v2.0
- ✅ Zero configuração
- ✅ Totalmente portátil

---

**Para compilar:** Execute `COMPILAR.bat`  
**Para testar:** Execute `python TESTAR_DISCOVERY.py`  
**Para usar:** Execute `dist/PDFgen.exe`

🌺 Plante Uma Flor v2.0

