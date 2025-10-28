// Sistema de Gerenciamento de Comandas - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-remover mensagens de alerta após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Validação de formulário de criação de pedido
    const form = document.querySelector('.pedido-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const horario = document.getElementById('horario').value;
            const dia_entrega = document.getElementById('dia_entrega').value;
            
            // Validar que a data de entrega não é no passado
            if (dia_entrega) {
                const hoje = new Date();
                hoje.setHours(0, 0, 0, 0);
                const dataEntrega = new Date(dia_entrega);
                
                if (dataEntrega < hoje) {
                    e.preventDefault();
                    alert('A data de entrega não pode ser no passado!');
                    return false;
                }
            }
            
            // Validar horário
            if (horario) {
                const regex = /^([01]?\d|2[0-3]):[0-5]\d$/;
                if (!regex.test(horario)) {
                    e.preventDefault();
                    alert('Formato de horário inválido. Use HH:MM (ex: 14:30)');
                    return false;
                }
            }
        });
    }

    // Atualizar quantidade automaticamente
    const quantidadeInput = document.getElementById('quantidade');
    if (quantidadeInput) {
        quantidadeInput.addEventListener('input', function(e) {
            let value = parseInt(e.target.value) || 0;
            if (value < 0) {
                e.target.value = 0;
            }
        });
    }

    // Confirmar deleção de pedidos
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Tem certeza que deseja deletar este pedido? Esta ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });

    // Atualização automática de status
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const form = this.closest('.status-form');
            if (form && confirm('Deseja atualizar o status do pedido?')) {
                form.submit();
            }
        });
    });

    // Animação de entrada dos cards
    const cards = document.querySelectorAll('.pedido-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Funcionalidade de busca (se implementada no futuro)
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const pedidoCards = document.querySelectorAll('.pedido-card');
            
            pedidoCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Melhorar UX com loading states
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Processando...';
            }
        });
    });
});

// API Helper functions (para uso futuro)
const API = {
    async criarPedido(data) {
        try {
            const response = await fetch('/api/pedidos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Erro ao criar pedido:', error);
            throw error;
        }
    },

    async listarPedidos() {
        try {
            const response = await fetch('/api/pedidos');
            return await response.json();
        } catch (error) {
            console.error('Erro ao listar pedidos:', error);
            throw error;
        }
    }
};

// Console log para debug (apenas em desenvolvimento)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🚀 Sistema de Gerenciamento de Comandas - Pronto!');
}

