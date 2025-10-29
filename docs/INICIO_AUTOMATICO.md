# Início Automático do Servidor

## Visão Geral

Configure o servidor para iniciar automaticamente quando o computador liga, rodando em background sem janelas visíveis.

---

## Arquivos Disponíveis

### Para HTTP

- `backend/iniciar_servidor.bat` - Inicia em janela minimizada
- `backend/iniciar_servidor_invisivel.vbs` - Inicia invisível (recomendado)
- `backend/parar_servidor.bat` - Para o servidor

### Para HTTPS

- `backend/iniciar_servidor_https.bat` - HTTPS em janela minimizada
- `backend/iniciar_servidor_https_invisivel.vbs` - HTTPS invisível (recomendado)
- `backend/abrir_sistema_https.bat` - Inicia + abre navegador

---

## Opção 1: Inicialização Automática do Windows (Recomendado)

### Configurar

**1. Abra a pasta de inicialização:**

Pressione `Win + R`, digite:
```
shell:startup
```

**2. Copie o arquivo desejado:**

Para HTTP:
```
backend/iniciar_servidor_invisivel.vbs
```

Para HTTPS:
```
backend/iniciar_servidor_https_invisivel.vbs
```

**3. Cole na pasta que abriu**

Pronto! O servidor iniciará automaticamente ao ligar o PC.

### Remover

Para desativar, delete o arquivo da pasta de inicialização.

---

## Opção 2: Atalho na Área de Trabalho

### Criar Atalho

**1. Clique com botão direito na Área de Trabalho**

**2. Novo → Atalho**

**3. Procurar...**

Navegue até o arquivo:
- `backend/iniciar_servidor_invisivel.vbs` (HTTP)
- `backend/iniciar_servidor_https_invisivel.vbs` (HTTPS)

**4. Nomeie o atalho:**
```
Servidor Plante Uma Flor
```

**5. Finalizar**

Duplo clique no atalho inicia o servidor.

---

## Uso

### Iniciar Servidor

**HTTP:**
```
Duplo clique em: iniciar_servidor_invisivel.vbs
```

**HTTPS:**
```
Duplo clique em: iniciar_servidor_https_invisivel.vbs
```

### Parar Servidor

```
Duplo clique em: parar_servidor.bat
```

Ou use um dos scripts avançados:
- `parar_servidor_admin.bat` (com permissões de admin)
- `parar_tudo_incluindo_vbs.bat` (para tudo)

### Verificar se Está Rodando

**Método 1:**

Acesse no navegador:
```
http://localhost:5000
```

**Método 2:**

Gerenciador de Tarefas (`Ctrl + Shift + Esc`):
- Procure por `python.exe` na lista de processos

**Método 3:**

Execute:
```
backend/verificar_porta.bat
```

---

## Diferenças Entre os Scripts

| Script | Janela | Recomendado | Logs |
|--------|--------|-------------|------|
| `iniciar_servidor.bat` | Minimizada | Para debug | Visíveis |
| `iniciar_servidor_invisivel.vbs` | Invisível | Produção | Ocultos |
| `abrir_sistema.bat` | Abre navegador | Uso manual | Visíveis |

---

## Acessar o Sistema

Após iniciar o servidor:

**No mesmo computador:**
```
http://localhost:5000
```

**De outros dispositivos (mesma rede WiFi):**
```
http://192.168.1.XXX:5000
```

Substitua `XXX` pelo IP do servidor (veja com `ipconfig`).

---

## HTTPS

Para configurar HTTPS, veja [`docs/HTTPS.md`](HTTPS.md).

Vantagens do HTTPS:
- PWA instalável em todos os dispositivos
- Mais seguro
- Service Worker completo

---

## Troubleshooting

### Erro: "Python não reconhecido"

**Solução:**

1. Certifique-se que Python está instalado
2. Adicione Python ao PATH do Windows:
   - Painel de Controle → Sistema → Variáveis de Ambiente
   - Edite PATH e adicione: `C:\Python3X\`

### Servidor não inicia

**Soluções:**

1. Execute `parar_servidor.bat` primeiro
2. Tente iniciar novamente
3. Verifique se porta 5000 está livre:
   ```
   backend/verificar_porta.bat
   ```

### Porta 5000 ocupada

**Soluções:**

1. Pare o servidor:
   ```
   parar_servidor.bat
   ```

2. Ou force parada:
   ```
   parar_tudo_incluindo_vbs.bat
   ```

3. Verifique processos:
   ```
   verificar_processos_vbs.bat
   ```

### Múltiplos servidores rodando

Execute:
```
parar_tudo_incluindo_vbs.bat
```

Ou mate manualmente via Gerenciador de Tarefas:
1. `Ctrl + Shift + Esc`
2. Aba "Detalhes"
3. Finalize todos `python.exe` e `wscript.exe`

---

## Segurança

### Rede Local

Por padrão, o servidor aceita conexões de toda a rede local (`0.0.0.0`).

**Para restringir apenas ao localhost:**

Edite `backend/app/config.py`:
```python
HOST = '127.0.0.1'  # Apenas localhost
```

### Produção

Para ambiente de produção:

1. Use HTTPS (veja [`docs/HTTPS.md`](HTTPS.md))
2. Use servidor WSGI (Gunicorn, uWSGI)
3. Configure firewall
4. Use proxy reverso (Nginx)

---

## Logs

### Ver Logs (.bat)

Se usar arquivo `.bat`, a janela minimizada mostra os logs.

Para visualizar:
1. Abra Gerenciador de Tarefas
2. Procure "Servidor PWA" ou "python.exe"
3. Botão direito → "Maximizar"

### Ver Logs (.vbs)

Scripts `.vbs` rodam invisíveis, logs ficam ocultos.

Para debug, use o `.bat` ao invés do `.vbs`.

---

## Importante

- Scripts `.vbs` iniciam servidor **totalmente invisível** (sem janela)
- Para parar, **DEVE** usar `parar_servidor.bat`
- Servidor continua rodando mesmo fechando o navegador
- Não execute múltiplas vezes (cria múltiplos servidores)

---

## Recomendação

**Para uso diário:**

1. Configure inicialização automática (Opção 1)
2. Use script `.vbs` (invisível)
3. Configure HTTPS para rede local
4. Instale PWA em todos os dispositivos

---

**Plante Uma Flor** - Sistema de Gestão de Pedidos PWA  
Documentação atualizada: 2024

