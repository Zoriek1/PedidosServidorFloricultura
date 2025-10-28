# 🚀 Guia Rápido - Automação do Servidor Flask

## ⚡ Início Rápido

### Windows (Mais Fácil)

```powershell
cd Servidor
.\iniciar_automático.ps1
```

Ou clique duas vezes em `iniciar_automático.bat`

---

## 📋 O Que o Script Faz

✅ **Inicia automaticamente às 08:00**
✅ **Encerra automaticamente às 18:30**
✅ **Reinicia automaticamente se o servidor cair**
✅ **Monitora a cada 60 segundos**

---

## 🎯 Como Funciona

```
┌─────────────────────────────────┐
│  Você executa o script          │
└──────────────┬──────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Horário ≥ 08:00?    │
    └──────────┬───────────┘
               │
        ┌──────┴──────┐
        │             │
       SIM           NÃO
        │             │
        ▼             ▼
   Inicia       Aguarda 08:00
   Servidor     
        │
        ▼
┌──────────────────────┐
│  Loop contínuo      │
│  (a cada 60s)       │
│                      │
│  1. Servidor OK?    │
│  2. Horário OK?     │
│  3. Reinicia se     │
│     necessário      │
│  4. Encerra se      │
│     ≥ 18:30         │
└──────────────────────┘
```

---

## 🛑 Como Parar

Pressione `Ctrl+C` no terminal

---

## ⚙️ Personalizar Horários

Edite `iniciar_automático.py`:

```python
HORA_INICIO = dt_time(7, 0)    # Mudar para 07:00
HORA_FIM = dt_time(19, 0)      # Mudar para 19:00
CHECK_INTERVAL = 30            # Verificar a cada 30 segundos
```

---

## 🐛 Problemas?

### Erro: Python não encontrado
**Solução:** Instale Python e adicione ao PATH

### Servidor não inicia
**Solução:** Execute `pip install -r static/requirements.txt`

### Porta já em uso
**Solução:** Feche outros processos usando a porta 5000

---

## 📖 Documentação Completa

Para mais detalhes, veja:
- `AUTOMACAO_README.md` - Documentação completa
- `RESUMO_AUTOMACAO.md` - Resumo executivo

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

