# Certificado CA - Plante Uma Flor

## Informacoes do Servidor

- **Hostname:** Gestor-pedidos.local
- **Porta:** 5000
- **Acesso:** https://Gestor-pedidos.local:5000

---

## Como Instalar este Certificado

### Android

1. Copie o arquivo `rootCA.pem` para o celular
2. Abra **Configuracoes** > **Seguranca**
3. Toque em **Instalar certificado** ou **Credenciais**
4. Escolha **Certificado CA** > **Instalar mesmo assim**
5. Navegue ate o arquivo `rootCA.pem`
6. De um nome (ex: "Gestor Pedidos CA")
7. Pronto https://Gestor-pedidos.local:5000

### iOS / iPhone / iPad

1. Envie o arquivo `rootCA.pem` por email ou AirDrop
2. Abra o arquivo no dispositivo
3. Va em **Ajustes** > **Geral** > **Perfis**
4. Toque no perfil "mkcert"
5. Toque em **Instalar** (digite a senha se pedido)
6. Va em **Ajustes** > **Geral** > **Sobre** > **Confianca do Certificado**
7. Ative o certificado "mkcert"
8. Pronto https://Gestor-pedidos.local:5000

### Windows (Outros PCs)

1. Copie o arquivo `rootCA.pem` para o PC
2. Clique duas vezes no arquivo
3. Clique em **Instalar Certificado...**
4. Escolha **Maquina Local** > **Avançar**
5. Escolha **Colocar todos os certificados no repositorio a seguir**
6. Clique em **Procurar** > Selecione **Autoridades de Certificacao Raiz Confiaveis**
7. Clique em **Avançar** > **Concluir**
8. Confirme o aviso de seguranca
9. Pronto https://Gestor-pedidos.local:5000

---

## Solucao de Problemas

### "Certificado nao e confiavel" / "Sua conexao nao e particular"

- Certifique-se de que o certificado foi instalado corretamente
- No Android/iOS, verifique se o certificado esta **ativo**
- Reinicie o navegador apos instalar

### "Nao consigo acessar o servidor"

- Certifique-se de estar na mesma rede que o servidor
- Teste primeiro via IP: https://[IP-DO-SERVIDOR]:5000
- Verifique se o servidor esta rodando

### "Nome nao pode ser resolvido" / "Hostname nao encontrado"

- mDNS pode nao funcionar em algumas redes
- Use o IP do servidor ao inves do hostname
- Em redes corporativas, pode estar bloqueado

---

**Gerado em:** 29/10/2025 10:32:38,63
**Servidor:** Gestor-pedidos.local
