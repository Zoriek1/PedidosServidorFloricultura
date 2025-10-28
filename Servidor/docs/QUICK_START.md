# 🚀 Quick Start - Plante Uma Flor v2.0

## Início Rápido (3 passos)

### 1️⃣ Primeira Vez? Execute Migration

```bash
python migrate_database.py
```

Isso preserva seus pedidos existentes e adiciona novos campos.

### 2️⃣ Testar o Sistema

```bash
python test_server.py
```

Deve mostrar: ✓ TODOS OS TESTES PASSARAM (5/5)

### 3️⃣ Iniciar o Servidor

**Windows:**
```bash
INICIAR_AQUI.bat
```

**Ou manualmente:**
```bash
python main.py
```

## ✅ Servidor Rodando!

Acesse em seu navegador:
- http://localhost:5000 (mesma máquina)
- http://192.168.x.x:5000 (outras máquinas na rede)

## 🔗 PDFgen.py (Cliente Desktop)

O cliente desktop **encontra automaticamente** o servidor!

Nenhuma configuração de IP necessária. ✨

## 📊 O Que Você Verá

✨ Painel moderno com gradiente roxo
📊 Estatísticas em tempo real
🔍 Filtros e busca
⚠️ Alertas de pedidos atrasados
🎯 Atualização automática a cada 30s

## ❓ Problemas?

### Erro: "no such column"
```bash
python migrate_database.py
```

### Testes falhando
```bash
# Verificar dependências
pip install -r requirements.txt
```

### Cliente não encontra servidor
1. Mesma rede? ✓
2. Firewall bloqueando? Liberar porta 5000 (TCP) e 37020 (UDP)
3. Testar com IP direto: http://192.168.x.x:5000

## 📝 Logs

Consulte: `logs/server_YYYYMMDD.log`

---

**Tudo pronto!** Seu sistema está rodando na versão 2.0 🎉

