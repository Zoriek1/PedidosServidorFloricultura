/**
 * Plante Uma Flor - PWA v3.0
 * Modal Component - Modais de confirmação e diálogo
 */

const Modal = {
    currentModal: null,

    /**
     * Mostra modal de confirmação
     * @param {Object} options - Opções do modal
     * @returns {Promise} Resolve com true se confirmado, false se cancelado
     */
    confirm(options = {}) {
        const {
            title = 'Confirmar',
            message = 'Tem certeza?',
            confirmText = 'Confirmar',
            cancelText = 'Cancelar',
            confirmClass = 'btn-danger',
            icon = 'fa-question-circle'
        } = options;

        return new Promise((resolve) => {
            const modal = this.create({
                title,
                message,
                icon,
                buttons: [
                    {
                        text: cancelText,
                        class: 'btn-secondary',
                        onClick: () => {
                            this.close(modal);
                            resolve(false);
                        }
                    },
                    {
                        text: confirmText,
                        class: confirmClass,
                        onClick: () => {
                            this.close(modal);
                            resolve(true);
                        }
                    }
                ]
            });

            this.show(modal);
        });
    },

    /**
     * Mostra modal de alerta
     */
    alert(options = {}) {
        const {
            title = 'Atenção',
            message = '',
            okText = 'OK',
            icon = 'fa-info-circle'
        } = options;

        return new Promise((resolve) => {
            const modal = this.create({
                title,
                message,
                icon,
                buttons: [
                    {
                        text: okText,
                        class: 'btn-primary',
                        onClick: () => {
                            this.close(modal);
                            resolve(true);
                        }
                    }
                ]
            });

            this.show(modal);
        });
    },

    /**
     * Cria estrutura do modal
     */
    create(options) {
        const {
            title,
            message,
            icon,
            buttons = []
        } = options;

        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';

        const content = document.createElement('div');
        content.className = 'modal-content';

        // Ícone
        let iconHtml = '';
        if (icon) {
            iconHtml = `
                <div class="text-center mb-4">
                    <i class="fas ${icon} text-5xl text-primary"></i>
                </div>
            `;
        }

        // Título
        const titleHtml = title ? `<h3 class="text-xl font-bold text-gray-800 mb-2">${Utils.escapeHtml(title)}</h3>` : '';

        // Mensagem
        const messageHtml = message ? `<p class="text-gray-600 mb-6">${Utils.escapeHtml(message)}</p>` : '';

        // Botões
        const buttonsHtml = buttons.map(btn => {
            return `<button class="btn ${btn.class}" data-action="${btn.text}">${Utils.escapeHtml(btn.text)}</button>`;
        }).join('');

        content.innerHTML = `
            ${iconHtml}
            <div class="text-center">
                ${titleHtml}
                ${messageHtml}
            </div>
            <div class="flex gap-3 justify-end">
                ${buttonsHtml}
            </div>
        `;

        // Adicionar event listeners nos botões
        buttons.forEach(btn => {
            const button = content.querySelector(`[data-action="${btn.text}"]`);
            if (button) {
                button.addEventListener('click', btn.onClick);
            }
        });

        overlay.appendChild(content);

        // Fechar ao clicar no overlay
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                const cancelButton = buttons.find(b => b.text === 'Cancelar' || b.class.includes('secondary'));
                if (cancelButton) {
                    cancelButton.onClick();
                }
            }
        });

        // Fechar com ESC
        const escapeHandler = (e) => {
            if (e.key === 'Escape') {
                const cancelButton = buttons.find(b => b.text === 'Cancelar' || b.class.includes('secondary'));
                if (cancelButton) {
                    cancelButton.onClick();
                }
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);

        return overlay;
    },

    /**
     * Mostra modal
     */
    show(modal) {
        document.body.appendChild(modal);
        this.currentModal = modal;

        // Animação de entrada
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
    },

    /**
     * Fecha modal
     */
    close(modal) {
        if (!modal) {
            modal = this.currentModal;
        }

        if (modal) {
            modal.classList.remove('active');
            
            setTimeout(() => {
                modal.remove();
                if (this.currentModal === modal) {
                    this.currentModal = null;
                }
            }, 200);
        }
    },

    /**
     * Modal de confirmação de deleção
     */
    confirmDelete(itemName = 'este item') {
        return this.confirm({
            title: 'Confirmar Exclusão',
            message: `Tem certeza que deseja deletar ${itemName}? Esta ação não pode ser desfeita.`,
            confirmText: 'Deletar',
            cancelText: 'Cancelar',
            confirmClass: 'btn-danger',
            icon: 'fa-trash-alt'
        });
    },

    /**
     * Modal customizado com HTML
     */
    custom(htmlContent, onClose) {
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';

        const content = document.createElement('div');
        content.className = 'modal-content';
        content.innerHTML = htmlContent;

        overlay.appendChild(content);

        // Fechar ao clicar no overlay
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.close(overlay);
                if (onClose) onClose();
            }
        });

        // Botões de fechar
        content.querySelectorAll('[data-modal-close]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.close(overlay);
                if (onClose) onClose();
            });
        });

        this.show(overlay);

        return overlay;
    }
};

