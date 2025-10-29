# Scripts Utilitários

Esta pasta contém scripts **utilitários e avançados** para gerenciamento do servidor.

## 📁 Scripts Disponíveis

### Inicialização

**`iniciar_servidor.bat`**
- Inicia o servidor Flask em segundo plano (HTTP)
- Não abre o navegador automaticamente
- Útil para desenvolvimento

**`iniciar_servidor_https.bat`**
- Inicia o servidor Flask em segundo plano (HTTPS)
- Requer certificados SSL configurados
- Útil para testes de rede

**`iniciar_servidor_invisivel.vbs`**
- Inicia o servidor completamente invisível (HTTP)
- Sem janela do console
- Útil para inicialização automática do Windows

**`iniciar_servidor_https_invisivel.vbs`**
- Inicia o servidor completamente invisível (HTTPS)
- Sem janela do console
- Requer certificados SSL

---

### Parada do Servidor

**`parar_servidor.bat`**
- Para o servidor Flask normalmente
- Método padrão e seguro

**`parar_servidor_admin.bat`**
- Para o servidor com privilégios de administrador
- Útil quando o servidor não responde

**`parar_servidor_forcado.bat`**
- Força o encerramento do servidor
- Último recurso se outros métodos falharem

**`parar_tudo_incluindo_vbs.bat`**
- Para servidor + processos VBS
- Limpa todos os processos relacionados
- Útil após usar scripts invisíveis

---

### Verificação e Diagnóstico

**`verificar_porta.bat`**
- Verifica se a porta 5000 está em uso
- Mostra qual processo está usando
- Útil para troubleshooting

**`verificar_processos_vbs.bat`**
- Lista processos Python e VBS em execução
- Útil para debug de scripts invisíveis

---

## 💡 Quando Usar Cada Script

### Desenvolvimento
- Use: `iniciar_servidor.bat`
- Permite ver logs no console

### Produção/Inicialização Automática
- Use: `iniciar_servidor_invisivel.vbs`
- Servidor roda em background sem janelas

### Problemas com Servidor
1. Tente: `parar_servidor.bat`
2. Se não funcionar: `parar_servidor_admin.bat`
3. Último recurso: `parar_servidor_forcado.bat`
4. Se usou .vbs: `parar_tudo_incluindo_vbs.bat`

### Diagnóstico
- Porta ocupada: `verificar_porta.bat`
- Ver processos: `verificar_processos_vbs.bat`

---

## 📚 Documentação Relacionada

- **Uso diário:** Veja scripts em `run/`
- **HTTPS:** Veja documentação em `ssl/`
- **Inicialização automática:** Ver `docs/INICIO_AUTOMATICO.md`

---

**Plante Uma Flor** - PWA v3.1  
Scripts Utilitários e Avançados

