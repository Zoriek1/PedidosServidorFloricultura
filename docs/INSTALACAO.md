# Instalação do PWA

## O que é um PWA?

Um **PWA (Progressive Web App)** é um site que funciona como aplicativo nativo!

### Vantagens

- Aparece como um app no computador/celular
- Abre mais rápido que sites normais
- Funciona offline (sem internet)
- Tela cheia (sem barra do navegador)
- Não precisa baixar de lojas de apps
- Atualiza automaticamente

---

## Windows (Desktop)

### Navegadores Suportados

- Google Chrome (recomendado)
- Microsoft Edge (recomendado)
- Brave
- Firefox (suporte limitado)

### Instalação

1. Abra o navegador
2. Acesse: `http://localhost:5000` (ou o IP da rede)
3. Procure o ícone de instalação na barra de endereços:
   - Ícone de computador [🖥️+]
   - Ou botão "Instalar"
4. Clique em "Instalar"
5. O app aparecerá:
   - No Menu Iniciar
   - Na Área de Trabalho (opcional)
   - Na barra de tarefas

### Uso

Após instalar:
- Aparece como um programa normal
- Abre em janela própria (sem navegador)
- Pode ser fixado na barra de tarefas
- Funciona offline

---

## Android

### Navegador Recomendado

Use o **Google Chrome** para melhor suporte a PWA.

### Instalação

1. Abra o Chrome no celular/tablet
2. Acesse: `http://IP:5000` (substitua pelo IP do servidor)
3. Duas opções:
   - **Opção A:** Banner "Adicionar à tela inicial" aparece automaticamente
   - **Opção B:** Menu (⋮) → "Adicionar à tela inicial" ou "Instalar app"
4. Confirme a instalação
5. Ícone aparecerá na tela inicial

### Uso

- Aparece como app nativo
- Abre em tela cheia
- Funciona offline
- Pode receber notificações

---

## iOS (iPhone/iPad)

### Navegador Requerido

**Importante:** Use apenas o **Safari** no iOS! Chrome e Firefox não suportam PWA no iPhone.

### Instalação

1. Abra o Safari
2. Acesse: `http://IP:5000`
3. Toque no botão "Compartilhar" (📤)
4. Role para baixo e toque em "Adicionar à Tela de Início"
5. Defina o nome: "Plante Uma Flor"
6. Toque em "Adicionar"

### Observações

- iOS tem suporte mais limitado a PWA
- Algumas features podem não funcionar
- Ainda assim é mais prático que acessar pelo navegador

---

## Acesso em Rede Local

### Descobrir IP do Servidor

No computador que roda o servidor:

```bash
ipconfig
```

Procure por "IPv4" (exemplo: `192.168.1.148`)

### Acessar de Outros Dispositivos

1. Conecte-se à mesma rede WiFi
2. No navegador, acesse: `http://IP:5000`
3. Instale como PWA no dispositivo

### Vantagens

- Todos na mesma rede podem acessar
- Funciona em qualquer dispositivo
- Cada um pode instalar como PWA
- Dados sincronizados em tempo real

---

## HTTPS (Recomendado)

Para instalar PWA em outros dispositivos da rede, use HTTPS:

1. Configure certificados SSL (veja [`docs/HTTPS.md`](HTTPS.md))
2. Acesse via `https://IP:5000`
3. Instale o PWA normalmente

**Benefícios:**
- PWA instalável em todos os dispositivos
- Cadeado verde no navegador
- Service Worker completo
- Mais seguro

---

## Desinstalar

### Windows

1. Método 1: Botão direito no app → "Desinstalar"
2. Método 2: Configurações → Apps → Procure "Plante Uma Flor" → Desinstalar

### Android

1. Segure o ícone do app
2. Arrastar para "Desinstalar" ou "Remover"

### iOS

1. Segure o ícone
2. Toque no "X" que aparece
3. Confirme remoção

---

## Alternativa: Atalho

Se não quiser instalar como PWA, crie um atalho que inicia automaticamente:

### Windows

Crie um arquivo `abrir_sistema.bat`:

```batch
@echo off
cd /d "%~dp0\backend"

REM Verificar se servidor está rodando
tasklist | find "python.exe" >nul 2>&1
if %errorlevel% neq 0 (
    start /MIN python main.py
    timeout /t 3 >nul
)

start http://localhost:5000
exit
```

Duplo clique abre o servidor + navegador automaticamente.

---

## PWA vs App Nativo

| Recurso | PWA | App Nativo (.exe) |
|---------|-----|-------------------|
| Instalação | Direto do navegador | Precisa baixar/instalar |
| Tamanho | ~500 KB | ~50-100 MB |
| Multiplataforma | Windows, Android, iOS, Linux | Apenas Windows |
| Atualizações | Automáticas | Manual |
| Offline | Sim | Sim |
| Performance | Rápido | Muito rápido |

---

## Conversão para Executável

### É Possível?

**Sim, mas não recomendado:**

Pode ser convertido usando Electron ou PyInstaller, porém:

**Desvantagens:**
- Arquivo muito maior (50+ MB)
- Só funciona no Windows
- Precisa incluir Python + bibliotecas
- Mais complexo de distribuir

**PWA é melhor porque:**
- Mais leve e rápido
- Funciona em qualquer dispositivo
- Atualiza automaticamente
- Mais fácil de distribuir

---

## Troubleshooting

### Botão de instalar não aparece

- Limpe o cache: `Ctrl + F5`
- Certifique-se que está em HTTPS (para rede local)
- Verifique se os ícones do PWA existem
- Feche e abra o navegador

### PWA não funciona offline

- Verifique se Service Worker está registrado
- Abra DevTools (F12) → Application → Service Workers
- Veja se há erros no console

### Erro ao acessar de outro dispositivo

- Confirme que está na mesma rede WiFi
- Verifique o firewall (porta 5000)
- Para HTTPS, instale o certificado raiz

---

## Recomendação Final

**Para melhor experiência:**

1. Configure HTTPS (veja [`docs/HTTPS.md`](HTTPS.md))
2. Instale como PWA em todos os dispositivos
3. Configure início automático do servidor ([`docs/INICIO_AUTOMATICO.md`](INICIO_AUTOMATICO.md))
4. Fixe o app na barra de tarefas/tela inicial

---

**Plante Uma Flor** - Sistema de Gestão de Pedidos PWA  
Documentação atualizada: 2024

