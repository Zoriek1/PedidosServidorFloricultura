/**
 * Plante Uma Flor v2.0 - JavaScript Otimizado
 * Sistema de gestão de pedidos com automação
 */

// Configurações globais
const CONFIG = {
    autoRefreshInterval: 30000, // 30 segundos
    notificationDuration: 3000,
    apiTimeout: 10000
};

// Estado da aplicação
const AppState = {
    pedidos: [],
    filtros: {
        status: '',
        busca: ''
    },
    isLoading: false
};

// Utilitários
const Utils = {
    // Debounce para otimizar buscas
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Formatar data
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    },

    // Formatar horário
    formatTime(timeString) {
        return timeString;
    },

    // Verificar se pedido está atrasado
    isOverdue(deliveryDate, deliveryTime) {
        const now = new Date();
        const delivery = new Date(`${deliveryDate}T${deliveryTime}`);
        return delivery < now;
    },

    // Mostrar notificação
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, CONFIG.notificationDuration);
    },

    // Fazer requisição HTTP
    async fetch(url, options = {}) {
        const defaultOptions = {
            timeout: CONFIG.apiTimeout,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const mergedOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    }
};

// Gerenciador de pedidos
const PedidoManager = {
    // Atualizar status do pedido
    async atualizarStatus(pedidoId, novoStatus) {
        try {
            AppState.isLoading = true;
            
            const response = await Utils.fetch(`/pedido/${pedidoId}/atualizar-status`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `status=${novoStatus}`
            });
            
            if (response.success) {
                // Atualizar interface
                this.updatePedidoInUI(pedidoId, { status: novoStatus });
                Utils.showNotification('Status atualizado com sucesso!', 'success');
            } else {
                throw new Error(response.error || 'Erro desconhecido');
            }
        } catch (error) {
            console.error('Erro ao atualizar status:', error);
            Utils.showNotification(`Erro ao atualizar status: ${error.message}`, 'error');
        } finally {
            AppState.isLoading = false;
        }
    },

    // Deletar pedido
    async deletarPedido(pedidoId) {
        try {
            AppState.isLoading = true;
            
            const response = await Utils.fetch(`/pedido/${pedidoId}/deletar`, {
                method: 'POST'
            });
            
            if (response.success) {
                // Remover da interface
                this.removePedidoFromUI(pedidoId);
                Utils.showNotification('Pedido deletado com sucesso!', 'success');
                this.updatePedidosCount();
            } else {
                throw new Error(response.error || 'Erro desconhecido');
            }
        } catch (error) {
            console.error('Erro ao deletar pedido:', error);
            Utils.showNotification(`Erro ao deletar pedido: ${error.message}`, 'error');
        } finally {
            AppState.isLoading = false;
        }
    },

    // Limpar pedidos antigos
    async limparPedidosAntigos() {
        try {
            AppState.isLoading = true;
            
            const response = await Utils.fetch('/limpar-antigos', {
                method: 'POST'
            });
            
            if (response.success) {
                Utils.showNotification(`${response.count} pedidos antigos removidos!`, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                throw new Error(response.error || 'Erro desconhecido');
            }
        } catch (error) {
            console.error('Erro ao limpar pedidos:', error);
            Utils.showNotification(`Erro ao limpar pedidos: ${error.message}`, 'error');
        } finally {
            AppState.isLoading = false;
        }
    },

    // Atualizar pedido na interface
    updatePedidoInUI(pedidoId, updates) {
        const pedidoCard = document.querySelector(`[data-id="${pedidoId}"]`);
        if (!pedidoCard) return;

        // Atualizar classe de status
        if (updates.status) {
            pedidoCard.className = `pedido-card status-${updates.status}`;
            pedidoCard.setAttribute('data-status', updates.status);
            
            const statusBadge = pedidoCard.querySelector('.status-badge');
            if (statusBadge) {
                statusBadge.textContent = updates.status.charAt(0).toUpperCase() + updates.status.slice(1);
            }
        }
    },

    // Remover pedido da interface
    removePedidoFromUI(pedidoId) {
        const pedidoCard = document.querySelector(`[data-id="${pedidoId}"]`);
        if (pedidoCard) {
            pedidoCard.remove();
        }
    },

    // Atualizar contador de pedidos
    updatePedidosCount() {
        const visiblePedidos = document.querySelectorAll('.pedido-card:not([style*="none"])');
        const countElement = document.getElementById('pedidos-count');
        if (countElement) {
            countElement.textContent = visiblePedidos.length;
        }
    }
};

// Gerenciador de filtros
const FilterManager = {
    // Aplicar filtros
    aplicarFiltros() {
        const searchTerm = document.getElementById('search-input')?.value.toLowerCase() || '';
        const statusFilter = document.getElementById('status-filter')?.value || '';
        
        AppState.filtros.busca = searchTerm;
        AppState.filtros.status = statusFilter;
        
        const pedidos = document.querySelectorAll('.pedido-card');
        let visibleCount = 0;
        
        pedidos.forEach(pedido => {
            const status = pedido.getAttribute('data-status');
            const text = pedido.textContent.toLowerCase();
            
            const matchesSearch = !searchTerm || text.includes(searchTerm);
            const matchesStatus = !statusFilter || status === statusFilter;
            
            if (matchesSearch && matchesStatus) {
                pedido.style.display = 'block';
                visibleCount++;
            } else {
                pedido.style.display = 'none';
            }
        });
        
        this.updateCount(visibleCount);
    },

    // Atualizar contador
    updateCount(count) {
        const countElement = document.getElementById('pedidos-count');
        if (countElement) {
            countElement.textContent = count;
        }
    },

    // Limpar filtros
    limparFiltros() {
        const searchInput = document.getElementById('search-input');
        const statusFilter = document.getElementById('status-filter');
        
        if (searchInput) searchInput.value = '';
        if (statusFilter) statusFilter.value = '';
        
        this.aplicarFiltros();
    }
};

// Gerenciador de modal
const ModalManager = {
    // Mostrar modal de confirmação
    mostrarModal(message, onConfirm) {
        const modal = document.getElementById('confirmModal');
        const messageElement = document.getElementById('modal-message');
        const confirmButton = document.getElementById('modal-confirm');
        
        if (!modal || !messageElement || !confirmButton) return;
        
        messageElement.textContent = message;
        confirmButton.onclick = () => {
            onConfirm();
            this.fecharModal();
        };
        
        modal.style.display = 'flex';
    },

    // Fechar modal
    fecharModal() {
        const modal = document.getElementById('confirmModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
};

// Gerenciador de automação
const AutomationManager = {
    // Verificar pedidos atrasados
    verificarPedidosAtrasados() {
        const pedidosAtrasados = document.querySelectorAll('.overdue-badge');
        if (pedidosAtrasados.length > 0) {
            // Destacar pedidos atrasados
            pedidosAtrasados.forEach(badge => {
                const pedidoCard = badge.closest('.pedido-card');
                if (pedidoCard) {
                    pedidoCard.classList.add('overdue-highlight');
                }
            });
            
            // Mostrar notificação se houver muitos atrasados
            if (pedidosAtrasados.length > 3) {
                Utils.showNotification(
                    `${pedidosAtrasados.length} pedidos atrasados precisam de atenção!`,
                    'error'
                );
            }
        }
    },

    // Auto-atualização
    iniciarAutoAtualizacao() {
        setInterval(() => {
            if (!AppState.isLoading) {
                this.verificarPedidosAtrasados();
            }
        }, CONFIG.autoRefreshInterval);
    }
};

// Event listeners globais
const EventListeners = {
    // Configurar listeners
    setup() {
        // Filtro de status
        const statusFilter = document.getElementById('status-filter');
        if (statusFilter) {
            statusFilter.addEventListener('change', () => {
                FilterManager.aplicarFiltros();
            });
        }

        // Campo de busca
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', Utils.debounce(() => {
                FilterManager.aplicarFiltros();
            }, 300));
        }

        // Botões de ação
        this.setupActionButtons();
        
        // Modal
        this.setupModalEvents();
    },

    // Configurar botões de ação
    setupActionButtons() {
        // Botão de limpar antigos
        const limparButton = document.querySelector('[onclick="limparPedidosAntigos()"]');
        if (limparButton) {
            limparButton.onclick = () => {
                ModalManager.mostrarModal(
                    'Tem certeza que deseja remover pedidos concluídos há mais de 24 horas?',
                    () => PedidoManager.limparPedidosAntigos()
                );
            };
        }

        // Botão de atualizar
        const atualizarButton = document.querySelector('[onclick="atualizarPainel()"]');
        if (atualizarButton) {
            atualizarButton.onclick = () => {
                location.reload();
            };
        }
    },

    // Configurar eventos do modal
    setupModalEvents() {
        const modal = document.getElementById('confirmModal');
        if (modal) {
            // Fechar ao clicar fora
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    ModalManager.fecharModal();
                }
            });

            // Fechar com ESC
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && modal.style.display === 'flex') {
                    ModalManager.fecharModal();
                }
            });
        }
    }
};

// Funções globais para compatibilidade com HTML
window.atualizarStatus = (pedidoId, novoStatus) => {
    PedidoManager.atualizarStatus(pedidoId, novoStatus);
};

window.deletarPedido = (pedidoId) => {
    ModalManager.mostrarModal(
        'Tem certeza que deseja deletar este pedido?',
        () => PedidoManager.deletarPedido(pedidoId)
    );
};

window.limparPedidosAntigos = () => {
    ModalManager.mostrarModal(
        'Tem certeza que deseja remover pedidos concluídos há mais de 24 horas?',
        () => PedidoManager.limparPedidosAntigos()
    );
};

window.atualizarPainel = () => {
    location.reload();
};

window.filtrarPorStatus = () => {
    FilterManager.aplicarFiltros();
};

window.buscarPedidos = () => {
    FilterManager.aplicarFiltros();
};

window.fecharModal = () => {
    ModalManager.fecharModal();
};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    console.log('Plante Uma Flor v2.0 - Painel de Gestão carregado');
    
    // Configurar event listeners
    EventListeners.setup();
    
    // Aplicar filtros iniciais
    FilterManager.aplicarFiltros();
    
    // Iniciar automação
    AutomationManager.iniciarAutoAtualizacao();
    
    // Verificar pedidos atrasados imediatamente
    AutomationManager.verificarPedidosAtrasados();
    
    console.log('Sistema inicializado com sucesso');
});

// Exportar para uso global
window.PlanteUmaFlor = {
    Utils,
    PedidoManager,
    FilterManager,
    ModalManager,
    AutomationManager,
    AppState
};