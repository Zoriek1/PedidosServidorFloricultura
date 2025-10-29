/**
 * Plante Uma Flor - PWA v3.0
 * Aplicação Principal
 */

const App = {
    version: '3.0.0',
    initialized: false,

    /**
     * Inicializa a aplicação
     */
    async init() {
        if (this.initialized) {
            console.warn('App já inicializado');
            return;
        }

        console.log(`🌺 Plante Uma Flor PWA v${this.version}`);
        console.log('Inicializando aplicação...');

        try {
            // Inicializar IndexedDB
            await DB.init();
            console.log('✅ IndexedDB inicializado');

            // Verificar conectividade
            this.checkConnectivity();

            // Configurar listeners globais
            this.setupGlobalListeners();

            // Verificar por atualizações do Service Worker
            this.checkForUpdates();

            // Prompt de instalação PWA
            this.setupInstallPrompt();

            this.initialized = true;
            console.log('✅ Aplicação inicializada com sucesso');

            // Mostrar notificação de boas-vindas
            setTimeout(() => {
                if (!sessionStorage.getItem('welcomed')) {
                    Notification.success('Bem-vindo ao Plante Uma Flor! 🌺');
                    sessionStorage.setItem('welcomed', 'true');
                }
            }, 1000);

        } catch (error) {
            console.error('❌ Erro ao inicializar aplicação:', error);
            Notification.error('Erro ao inicializar aplicação');
        }
    },

    /**
     * Verifica conectividade e sincroniza dados
     */
    async checkConnectivity() {
        if (Utils.isOnline()) {
            console.log('✅ Online - Sincronizando dados...');
            
            try {
                // Sincronizar pedidos pendentes do IndexedDB
                await DB.syncPendingPedidos();
                
                // Verificar health do servidor
                const health = await API.healthCheck();
                if (health.success) {
                    console.log('✅ Servidor acessível');
                }
            } catch (error) {
                console.warn('⚠️ Erro ao verificar conectividade:', error);
            }
        } else {
            console.log('⚠️ Offline - Modo offline ativado');
            Notification.warning('Você está offline. As alterações serão sincronizadas quando voltar online.');
        }
    },

    /**
     * Configura listeners globais
     */
    setupGlobalListeners() {
        // Online/Offline events
        window.addEventListener('online', () => {
            console.log('✅ Conexão restaurada');
            this.checkConnectivity();
        });

        window.addEventListener('offline', () => {
            console.log('⚠️ Conexão perdida');
        });

        // Antes de sair da página
        window.addEventListener('beforeunload', (e) => {
            // Verificar se há pedidos pendentes
            DB.getPendingPedidos().then(pending => {
                if (pending.length > 0) {
                    e.preventDefault();
                    e.returnValue = 'Você tem pedidos pendentes de sincronização. Tem certeza que deseja sair?';
                }
            });
        });

        // Atalhos de teclado
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K: Buscar
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.getElementById('search-input');
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // Ctrl/Cmd + N: Novo pedido
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                Router.navigate('/criar-pedido');
            }

            // Ctrl/Cmd + H: Home/Painel
            if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
                e.preventDefault();
                Router.navigate('/painel');
            }
        });

        // Visibilidade da página
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                // Página voltou a ser visível
                console.log('👁️ Página visível novamente');
                
                // Recarregar dados se estiver no painel
                if (Router.currentRoute === '/painel' && typeof PainelManager !== 'undefined') {
                    PainelManager.loadPedidos();
                }
            }
        });
    },

    /**
     * Verifica por atualizações do Service Worker
     */
    checkForUpdates() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.ready.then(registration => {
                // Verificar por atualizações a cada 1 hora
                setInterval(() => {
                    registration.update();
                }, 60 * 60 * 1000);

                // Listener para nova versão disponível
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // Nova versão disponível
                            this.showUpdateNotification();
                        }
                    });
                });
            });
        }
    },

    /**
     * Mostra notificação de atualização disponível
     */
    showUpdateNotification() {
        const notification = Notification.info('Nova versão disponível! Clique para atualizar.', 999999);
        
        notification.addEventListener('click', () => {
            window.location.reload();
        });

        // Adicionar botão de atualizar
        const updateBtn = document.createElement('button');
        updateBtn.textContent = 'Atualizar';
        updateBtn.className = 'ml-2 px-3 py-1 bg-white text-blue-600 rounded hover:bg-gray-100';
        updateBtn.onclick = () => {
            window.location.reload();
        };
        notification.appendChild(updateBtn);
    },

    /**
     * Configura prompt de instalação PWA
     */
    setupInstallPrompt() {
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;

            // Verificar se já foi instalado ou prompt foi mostrado
            if (!localStorage.getItem('pwa-install-prompt-shown')) {
                this.showInstallBanner(deferredPrompt);
            }
        });

        // Detectar quando app é instalado
        window.addEventListener('appinstalled', () => {
            console.log('✅ PWA instalado!');
            Notification.success('App instalado com sucesso! 🎉');
            deferredPrompt = null;
        });
    },

    /**
     * Mostra banner de instalação
     */
    showInstallBanner(deferredPrompt) {
        const banner = document.createElement('div');
        banner.className = 'fixed bottom-20 left-4 right-4 bg-primary text-white p-4 rounded-lg shadow-xl z-50 animate-fade-in';
        banner.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex-1">
                    <p class="font-semibold">Instalar Plante Uma Flor</p>
                    <p class="text-sm opacity-90">Adicione à tela inicial para acesso rápido</p>
                </div>
                <div class="flex gap-2 ml-4">
                    <button id="install-dismiss" class="px-3 py-1 bg-white bg-opacity-20 rounded hover:bg-opacity-30 transition">
                        Depois
                    </button>
                    <button id="install-app" class="px-3 py-1 bg-white text-primary rounded hover:bg-gray-100 transition">
                        Instalar
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(banner);

        // Botão Instalar
        document.getElementById('install-app').addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log(`Install prompt outcome: ${outcome}`);
                
                localStorage.setItem('pwa-install-prompt-shown', 'true');
                banner.remove();
            }
        });

        // Botão Depois
        document.getElementById('install-dismiss').addEventListener('click', () => {
            banner.remove();
            localStorage.setItem('pwa-install-prompt-shown', 'true');
        });

        // Auto-remover após 10 segundos
        setTimeout(() => {
            if (banner.parentElement) {
                banner.remove();
            }
        }, 10000);
    },

    /**
     * Limpa cache e dados locais
     */
    async clearAllData() {
        const confirmed = await Modal.confirm({
            title: 'Limpar Todos os Dados',
            message: 'Isso vai limpar o cache e dados locais. Tem certeza?',
            confirmText: 'Limpar',
            cancelText: 'Cancelar'
        });

        if (confirmed) {
            try {
                // Limpar IndexedDB
                await DB.clearAll();

                // Limpar Cache do Service Worker
                if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
                    navigator.serviceWorker.controller.postMessage({
                        type: 'CLEAR_CACHE'
                    });
                }

                // Limpar Storage
                localStorage.clear();
                sessionStorage.clear();

                Notification.success('Dados limpos com sucesso!');
                
                // Recarregar após 1 segundo
                setTimeout(() => {
                    window.location.reload();
                }, 1000);

            } catch (error) {
                console.error('Erro ao limpar dados:', error);
                Notification.error('Erro ao limpar dados');
            }
        }
    }
};

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}

// Expor App globalmente para debug
window.App = App;

