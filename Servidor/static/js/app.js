/**
 * Plante Uma Flor v2.0 - JavaScript Modular
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

// ============================================
// Utilit ários
// ============================================
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

    // Mostrar notificação toast
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, CONFIG.notificationDuration);
    },

    // Fazer requisição HTTP com tratamento de erros
    async fetchAPI(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    ...options.headers
                }
            });
            
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

// ============================================
// Gerenciador de Pedidos
// ============================================
const PedidoManager = {
    // Atualizar status do pedido
    async atualizarStatus(pedidoId, novoStatus) {
        try {
            AppState.isLoading = true;
            
            const response = await fetch(`/pedido/${pedidoId}/atualizar-status`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `status=${novoStatus}`
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Atualizar interface
                this.updatePedidoInUI(pedidoId, { status: novoStatus });
                Utils.showNotification('Status atualizado com sucesso!', 'success');
            } else {
                throw new Error(result.error || 'Erro desconhecido');
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
            
            const response = await fetch(`/pedido/${pedidoId}/deletar`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Remover da interface
                this.removePedidoFromUI(pedidoId);
                Utils.showNotification('Pedido deletado com sucesso!', 'success');
                this.updatePedidosCount();
            } else {
                throw new Error(result.error || 'Erro desconhecido');
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
            
            const response = await fetch('/limpar-antigos', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                Utils.showNotification(`${result.count} pedidos antigos removidos!`, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                throw new Error(result.error || 'Erro desconhecido');
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
            // Remover classes antigas de status
            pedidoCard.className = pedidoCard.className.replace(/status-\w+/g, '');
            pedidoCard.classList.add(`status-${updates.status}`);
            pedidoCard.setAttribute('data-status', updates.status);
            
            // Atualizar badge de status
            const statusBadge = pedidoCard.querySelector('.status-badge');
            if (statusBadge) {
                statusBadge.className = `status-badge status-${updates.status}`;
                // Formatar texto do status
                const statusText = updates.status
                    .replace(/_/g, ' ')
                    .split(' ')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');
                statusBadge.textContent = statusText;
            }
        }
    },

    // Remover pedido da interface
    removePedidoFromUI(pedidoId) {
        const pedidoCard = document.querySelector(`[data-id="${pedidoId}"]`);
        if (pedidoCard) {
            pedidoCard.style.opacity = '0';
            setTimeout(() => pedidoCard.remove(), 300);
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

// ============================================
// Gerenciador de Filtros
// ============================================
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

// ============================================
// Gerenciador de Modal
// ============================================
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

// ============================================
// Gerenciador de Automação
// ============================================
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
                console.warn(`${pedidosAtrasados.length} pedidos atrasados!`);
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

// ============================================
// Event Listeners
// ============================================
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

        // Modal - fechar ao clicar fora
        const modal = document.getElementById('confirmModal');
        if (modal) {
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

// ============================================
// Funções Globais (compatibilidade com HTML)
// ============================================
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

// ============================================
// Inicialização da Aplicação
// ============================================
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

