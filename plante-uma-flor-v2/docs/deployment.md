# Plante Uma Flor v2.0 - Guia de Deploy

## 🚀 Instalação e Configuração

### 1. Configuração Inicial

```bash
# Clonar ou baixar o projeto
cd plante-uma-flor-v2

# Executar configuração automática
python scripts/setup.py
```

### 2. Configuração Manual (Alternativa)

```bash
# Instalar dependências do cliente
cd client
pip install -r src/build/requirements.txt

# Instalar dependências do servidor
cd ../server
pip install -r src/requirements.txt

# Criar diretórios necessários
mkdir -p client/logs client/dist server/logs server/database
```

## 🖥️ Executando o Sistema

### Servidor (Escritório)

```bash
# Desenvolvimento
cd server
python src/main.py

# Produção
cd server
python scripts/start_server.py
```

**Acesso:** http://localhost:5000

### Cliente (Ateliê)

```bash
# Desenvolvimento
cd client
python src/main.py

# Executável (após build)
cd client/dist
./PlanteUmaFlor-Client.exe
```

## 🔧 Build do Executável

### Build Automático

```bash
cd client
python src/build/build_exe.py
```

### Build Manual com PyInstaller

```bash
cd client
pyinstaller --onefile --windowed --name=PlanteUmaFlor-Client src/main.py
```

### Build com Nuitka (Mais Otimizado)

```bash
cd client
nuitka --standalone --windows-disable-console src/main.py
```

## 🌐 Configuração de Rede

### IP do Servidor

Edite o arquivo `client/src/resources/config.json`:

```json
{
  "server": {
    "base_url": "http://192.168.1.148:5000"
  }
}
```

### Firewall

- **Porta 5000**: Deve estar aberta no servidor
- **Cliente**: Não precisa de portas abertas

## 🔒 Segurança

### Medidas Implementadas

1. **Criação via Web BLOQUEADA**: Apenas cliente desktop pode criar pedidos
2. **Autenticação API**: Sistema de chaves para API
3. **Validação de Dados**: Validação rigorosa em todos os endpoints
4. **Logs de Segurança**: Todas as ações são logadas

### Configurações de Segurança

```python
# server/src/app/config.py
SECURITY_ENABLED = True
API_AUTH_REQUIRED = True
WEB_CREATION_BLOCKED = True
```

## 📊 Monitoramento

### Logs

- **Cliente**: `client/logs/client_YYYYMMDD.log`
- **Servidor**: `server/logs/server_YYYYMMDD.log`

### Limpeza Automática

```bash
# Executar limpeza manual
cd server
python scripts/cleanup_old_pedidos.py
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Cliente não conecta ao servidor**
   - Verificar IP do servidor
   - Verificar firewall
   - Verificar se servidor está rodando

2. **Erro de permissão no Windows**
   - Executar como administrador
   - Verificar antivírus

3. **PDF não é gerado**
   - Verificar permissões da pasta Documents
   - Verificar fontes instaladas

### Logs de Debug

```bash
# Verificar logs do cliente
tail -f client/logs/client_*.log

# Verificar logs do servidor
tail -f server/logs/server_*.log
```

## 🔄 Atualizações

### Backup Antes de Atualizar

```bash
# Backup do banco de dados
cp server/database/pedidos.db server/database/pedidos_backup.db

# Backup dos logs
tar -czf logs_backup.tar.gz client/logs server/logs
```

### Processo de Atualização

1. Parar servidor e cliente
2. Fazer backup
3. Atualizar código
4. Executar `python scripts/setup.py`
5. Reiniciar sistema

## 📈 Performance

### Otimizações Implementadas

1. **Cliente**:
   - Carregamento lazy de módulos
   - Cache de fontes
   - Interface otimizada

2. **Servidor**:
   - Conexões de banco otimizadas
   - Limpeza automática
   - Logs rotativos

### Monitoramento de Performance

```bash
# Verificar uso de memória
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"

# Verificar espaço em disco
python -c "import shutil; print(f'Disco: {shutil.disk_usage(\".\").free // (1024**3)} GB livres')"
```

## 🆘 Suporte

### Informações do Sistema

```bash
# Executar diagnóstico
python scripts/test_integration.py
```

### Contato

- **Sistema**: Plante Uma Flor v2.0
- **Versão**: 2.0.0
- **Compatibilidade**: Windows 10/11, Python 3.7+