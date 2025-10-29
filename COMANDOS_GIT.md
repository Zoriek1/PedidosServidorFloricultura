# Comandos Git para Nova Branch

Este arquivo contém os comandos para criar a branch `gestor-web-pwa` com apenas o código do PWA.

---

## Pré-requisitos

1. Certifique-se de que todos os arquivos estão commitados na branch atual
2. Verifique se está no repositório correto

```bash
git status
git log --oneline -5
```

---

## Comandos PowerShell (Windows)

Execute os comandos abaixo no PowerShell, na raiz do repositório:

```powershell
# Navegar para raiz do repositório
cd "C:\Gestor de Pedidos Plante uma flor"

# Verificar status
git status

# Criar nova branch
git checkout -b gestor-web-pwa

# Remover pastas antigas (Clientes e Servidor)
git rm -r Clientes/
git rm -r Servidor/

# Mover conteúdo de PWA/ para raiz
# PowerShell
Get-ChildItem -Path PWA -Force | Move-Item -Destination .
Remove-Item PWA

# Adicionar arquivos
git add .

# Commit com mensagem descritiva
git commit -m "feat: Implementação completa do Gestor Web (PWA v3.1)

Sistema moderno de gestão de pedidos como Progressive Web App

Características:
- Progressive Web App multiplataforma (Windows, Android, iOS)
- Interface responsiva e moderna
- Suporte offline completo com Service Worker
- Sincronização automática via IndexedDB
- HTTPS configurável para rede local
- Impressão profissional de pedidos em A4
- REST API completa
- Painel com filtros e busca em tempo real

Tecnologias:
- Backend: Flask + SQLAlchemy + SQLite
- Frontend: HTML5 + Tailwind CSS + JavaScript ES6+
- PWA: Service Worker + Manifest + IndexedDB
- HTTPS: mkcert para certificados locais

Migração completa do sistema desktop Tkinter para PWA web moderna."

# Push para remoto
git push -u origin gestor-web-pwa
```

---

## Comandos Git Bash / Linux / Mac

```bash
# Navegar para raiz do repositório
cd "/c/Gestor de Pedidos Plante uma flor"  # Windows
# ou
cd ~/gestor-pedidos                         # Linux/Mac

# Verificar status
git status

# Criar nova branch
git checkout -b gestor-web-pwa

# Remover pastas antigas
git rm -r Clientes/
git rm -r Servidor/

# Mover conteúdo de PWA/ para raiz
mv PWA/* .
mv PWA/.gitignore .
rmdir PWA

# Adicionar arquivos
git add .

# Commit
git commit -m "feat: Implementação completa do Gestor Web (PWA v3.1)

Sistema moderno de gestão de pedidos como Progressive Web App

Características:
- Progressive Web App multiplataforma (Windows, Android, iOS)
- Interface responsiva e moderna
- Suporte offline completo com Service Worker
- Sincronização automática via IndexedDB
- HTTPS configurável para rede local
- Impressão profissional de pedidos em A4
- REST API completa
- Painel com filtros e busca em tempo real

Tecnologias:
- Backend: Flask + SQLAlchemy + SQLite
- Frontend: HTML5 + Tailwind CSS + JavaScript ES6+
- PWA: Service Worker + Manifest + IndexedDB
- HTTPS: mkcert para certificados locais

Migração completa do sistema desktop Tkinter para PWA web moderna."

# Push
git push -u origin gestor-web-pwa
```

---

## Verificar Estrutura Final

Após executar os comandos, a estrutura deve ficar:

```
gestor-web-pwa (branch)/
├── .gitignore
├── README.md
├── INICIO_RAPIDO.md
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── ssl/
│   │   ├── INSTALAR_MKCERT_SIMPLES.bat
│   │   ├── INSTALAR_MKCERT.bat
│   │   ├── GERAR_CERTIFICADOS_AUTO.bat
│   │   ├── GERAR_CERTIFICADOS_LOCAL.bat
│   │   └── GERAR_CERTIFICADOS.bat
│   ├── iniciar_servidor.bat
│   ├── iniciar_servidor_invisivel.vbs
│   ├── iniciar_servidor_https.bat
│   ├── iniciar_servidor_https_invisivel.vbs
│   ├── abrir_sistema.bat
│   ├── abrir_sistema_https.bat
│   ├── parar_servidor.bat
│   ├── parar_servidor_admin.bat
│   ├── parar_servidor_forcado.bat
│   ├── parar_tudo_incluindo_vbs.bat
│   ├── verificar_porta.bat
│   ├── verificar_processos_vbs.bat
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   ├── icons/
│   │   └── js/
│   ├── pages/
│   ├── index.html
│   ├── manifest.json
│   └── sw.js
└── docs/
    ├── HTTPS.md
    ├── INSTALACAO.md
    ├── DESENVOLVIMENTO.md
    └── INICIO_AUTOMATICO.md
```

Verifique com:
```bash
git ls-files
```

---

## Voltar para Branch Principal

Se precisar voltar para a branch principal:

```bash
git checkout main
# ou
git checkout master
```

---

## Atualizar Branch PWA

Se fizer alterações na branch principal e quiser atualizar a PWA:

```bash
# Na branch gestor-web-pwa
git merge main

# Ou rebase
git rebase main
```

---

## Deletar Branch (Se Necessário)

**CUIDADO:** Isso apaga a branch!

```bash
# Local
git branch -d gestor-web-pwa

# Remoto
git push origin --delete gestor-web-pwa
```

---

## Criar Pull Request

Após o push, crie um Pull Request no GitHub:

1. Acesse o repositório no GitHub
2. Verá banner: "Compare & pull request"
3. Clique e preencha:
   - **Título:** `feat: Sistema PWA para Gestão de Pedidos v3.1`
   - **Descrição:** Copie a mensagem do commit
4. Crie o PR

---

## Problemas Comuns

### Erro: "working tree has modifications"

```bash
git status
git stash  # Salva alterações
# Ou
git add .
git commit -m "WIP: salvando alterações"
```

### Erro: "branch already exists"

```bash
# Deletar e recriar
git branch -D gestor-web-pwa
git checkout -b gestor-web-pwa
```

### Erro ao mover arquivos

```powershell
# PowerShell - Forçar move
Get-ChildItem -Path PWA -Force | ForEach-Object {
    Move-Item -Path $_.FullName -Destination . -Force
}
```

---

## Verificações Finais

Antes de fazer push, verifique:

```bash
# Ver arquivos
git ls-files

# Ver status
git status

# Ver último commit
git log -1

# Ver diferenças
git diff main..gestor-web-pwa --stat
```

---

## Notas

- O `.gitignore` já está configurado para ignorar:
  - `database.db`
  - Certificados SSL (`*.pem`, `*.key`)
  - Logs (`*.log`)
  - Python cache (`__pycache__/`)
  - IDEs (`.vscode/`, `.idea/`)
  
- Arquivos **não versionados mas importantes**:
  - `backend/database.db` (banco de dados local)
  - `backend/ssl/*.pem` (certificados HTTPS)
  - `backend/logs/*.log` (logs do servidor)

---

**Plante Uma Flor** - Sistema de Gestão de Pedidos PWA  
Comandos Git para Branch Organizada

