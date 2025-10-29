/**
 * Plante Uma Flor - PWA v3.0
 * Form Manager - Gerenciador do formulário multi-step
 */

const FormManager = {
    currentStep: 1,
    totalSteps: 4,
    formData: {},

    /**
     * Inicializa o formulário
     */
    init() {
        console.log('📝 Inicializando formulário');
        
        // Carregar dados do rascunho se existir
        this.loadDraft();
        
        // Configurar listeners
        this.setupListeners();
        
        // Mostrar primeiro step
        this.showStep(1);
        
        // Atualizar progress bar
        this.updateProgress();
    },

    /**
     * Configura event listeners
     */
    setupListeners() {
        // Botões de navegação
        const btnAnterior = document.getElementById('btn-anterior');
        const btnProximo = document.getElementById('btn-proximo');
        const btnFinalizar = document.getElementById('btn-finalizar');

        console.log('🔧 Configurando listeners dos botões...');
        console.log('Botão Anterior:', btnAnterior ? 'Encontrado' : 'NÃO encontrado');
        console.log('Botão Próximo:', btnProximo ? 'Encontrado' : 'NÃO encontrado');
        console.log('Botão Finalizar:', btnFinalizar ? 'Encontrado' : 'NÃO encontrado');

        if (btnAnterior) {
            btnAnterior.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('⬅️ Clicou em Anterior');
                this.previousStep();
            });
        }

        if (btnProximo) {
            btnProximo.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('➡️ Clicou em Próximo');
                this.nextStep();
            });
        }

        if (btnFinalizar) {
            btnFinalizar.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('✅ Clicou em Finalizar');
                this.submitForm();
            });
            console.log('✅ Listener do botão Finalizar configurado!');
        } else {
            console.warn('⚠️ Botão Finalizar NÃO encontrado ao configurar listeners');
        }

        // Listener para tipo de pedido (Entrega/Retirada)
        document.querySelectorAll('input[name="tipo_pedido"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleEnderecoFields(e.target.value);
            });
        });

        // Verificar tipo inicial ao carregar
        const tipoInicial = document.querySelector('input[name="tipo_pedido"]:checked');
        if (tipoInicial) {
            this.toggleEnderecoFields(tipoInicial.value);
        }

        // Salvar rascunho automaticamente
        document.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('change', () => this.saveDraft());
        });

        // Auto-aplicar máscaras
        Masks.applyAll();
    },

    /**
     * Mostra/oculta campos de endereço baseado no tipo de pedido
     */
    toggleEnderecoFields(tipoPedido) {
        const enderecoContainer = document.getElementById('endereco')?.closest('div');
        const obsEntregaContainer = document.getElementById('obs_entrega')?.closest('div');
        const step3Title = document.querySelector('#step-3 h2');

        if (tipoPedido === 'Retirada') {
            // Esconder campos de endereço
            if (enderecoContainer) {
                enderecoContainer.style.display = 'none';
                // Remover required do endereço
                const enderecoField = document.getElementById('endereco');
                if (enderecoField) {
                    enderecoField.removeAttribute('required');
                    enderecoField.value = ''; // Limpar valor
                }
            }
            
            // Mudar título do step 3
            if (step3Title) {
                step3Title.innerHTML = `
                    <i class="fas fa-store text-primary"></i>
                    Observações de Retirada
                `;
            }

            // Manter observações visíveis e ajustar label
            if (obsEntregaContainer) {
                const label = obsEntregaContainer.querySelector('label');
                if (label) {
                    label.innerHTML = `
                        Como Retirar / Observações de Retirada
                    `;
                }
            }

            console.log('🏪 Modo: Retirada - Campos de endereço ocultados');
        } else {
            // Mostrar campos de endereço
            if (enderecoContainer) {
                enderecoContainer.style.display = 'block';
            }

            // Restaurar título do step 3
            if (step3Title) {
                step3Title.innerHTML = `
                    <i class="fas fa-map-marker-alt text-primary"></i>
                    Logística de Entrega
                `;
            }

            // Restaurar label de observações
            if (obsEntregaContainer) {
                const label = obsEntregaContainer.querySelector('label');
                if (label) {
                    label.innerHTML = `
                        Como Entregar / Observações de Entrega
                    `;
                }
            }

            console.log('🚚 Modo: Entrega - Campos de endereço visíveis');
        }
    },

    /**
     * Mostra step específico
     */
    showStep(step) {
        // Esconder todos os steps
        document.querySelectorAll('.form-step').forEach(s => {
            s.classList.remove('active');
        });

        // Mostrar step atual
        const currentStepElement = document.getElementById(`step-${step}`);
        if (currentStepElement) {
            currentStepElement.classList.add('active');
        }

        // IMPORTANTE: Atualizar currentStep ANTES de chamar updateButtons
        this.currentStep = step;
        
        // Atualizar botões (agora com currentStep correto)
        this.updateButtons();
        
        // Atualizar número do step
        const stepNumber = document.getElementById('step-number');
        if (stepNumber) {
            stepNumber.textContent = step;
        }

        // Se está indo para o step 3, garantir que campos de endereço estejam corretos
        if (step === 3) {
            const tipoSelecionado = document.querySelector('input[name="tipo_pedido"]:checked');
            if (tipoSelecionado) {
                this.toggleEnderecoFields(tipoSelecionado.value);
            }
        }

        // Scroll para o topo
        window.scrollTo(0, 0);

        console.log(`✅ Mudou para Step ${step}`);
    },

    /**
     * Atualiza botões de navegação
     */
    updateButtons() {
        const btnAnterior = document.getElementById('btn-anterior');
        const btnProximo = document.getElementById('btn-proximo');
        const btnFinalizar = document.getElementById('btn-finalizar');

        console.log(`🔄 Atualizando botões - Step ${this.currentStep}/${this.totalSteps}`);

        // Botão Anterior
        if (btnAnterior) {
            if (this.currentStep === 1) {
                btnAnterior.classList.add('hidden');
            } else {
                btnAnterior.classList.remove('hidden');
            }
        }

        // Botão Próximo
        if (btnProximo) {
            if (this.currentStep === this.totalSteps) {
                btnProximo.classList.add('hidden');
                console.log('🚫 Botão Próximo ESCONDIDO');
            } else {
                btnProximo.classList.remove('hidden');
                console.log('✅ Botão Próximo VISÍVEL');
            }
        }

        // Botão Finalizar
        if (btnFinalizar) {
            if (this.currentStep === this.totalSteps) {
                btnFinalizar.classList.remove('hidden');
                console.log('✅ Botão Finalizar VISÍVEL');
                
                // Reconfigurar listener para garantir
                const newBtn = btnFinalizar.cloneNode(true);
                btnFinalizar.parentNode.replaceChild(newBtn, btnFinalizar);
                newBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('✅ Clicou em Finalizar (listener recém-adicionado)');
                    this.submitForm();
                });
            } else {
                btnFinalizar.classList.add('hidden');
                console.log('🚫 Botão Finalizar ESCONDIDO');
            }
        } else {
            console.warn('⚠️ Botão Finalizar NÃO encontrado em updateButtons()');
        }
    },

    /**
     * Atualiza barra de progresso
     */
    updateProgress() {
        const progress = (this.currentStep / this.totalSteps) * 100;
        const progressBar = document.getElementById('progress-bar');
        
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }

        // Atualizar indicadores
        for (let i = 1; i <= this.totalSteps; i++) {
            const indicator = document.getElementById(`progress-${i}`);
            if (indicator) {
                if (i < this.currentStep) {
                    indicator.classList.add('completed');
                    indicator.classList.remove('active');
                } else if (i === this.currentStep) {
                    indicator.classList.add('active');
                    indicator.classList.remove('completed');
                } else {
                    indicator.classList.remove('active', 'completed');
                }
            }
        }
    },

    /**
     * Valida step atual
     */
    validateCurrentStep() {
        console.log(`🔍 Validando Step ${this.currentStep}...`);
        
        const currentStepElement = document.getElementById(`step-${this.currentStep}`);
        if (!currentStepElement) {
            console.log('⚠️ Step element não encontrado');
            return true;
        }

        const requiredFields = currentStepElement.querySelectorAll('[required]');
        console.log(`📋 Campos obrigatórios encontrados: ${requiredFields.length}`);
        
        let isValid = true;
        const errors = [];

        requiredFields.forEach(field => {
            const fieldName = field.getAttribute('data-field-name') || field.name || 'Campo';
            const validationType = field.getAttribute('data-validation') || 'required';
            
            console.log(`   - Validando campo: ${fieldName} (${field.id}) = "${field.value}"`);
            
            const result = Validators.validateField(field, validationType, fieldName);
            
            if (!result.valid) {
                isValid = false;
                errors.push(result.message);
                console.log(`   ❌ ${result.message}`);
                
                // Scroll para o primeiro erro
                if (errors.length === 1) {
                    Utils.scrollToElement(field);
                }
            } else {
                console.log(`   ✅ OK`);
            }
        });

        if (!isValid) {
            console.log(`❌ Validação FALHOU. Erros:`, errors);
            Notification.warning('Por favor, preencha todos os campos obrigatórios');
        } else {
            console.log(`✅ Validação PASSOU!`);
        }

        return isValid;
    },

    /**
     * Próximo step
     */
    nextStep() {
        if (this.validateCurrentStep()) {
            this.saveDraft();
            
            if (this.currentStep < this.totalSteps) {
                this.showStep(this.currentStep + 1);
                this.updateProgress();
            }
        }
    },

    /**
     * Step anterior
     */
    previousStep() {
        this.saveDraft();
        
        if (this.currentStep > 1) {
            this.showStep(this.currentStep - 1);
            this.updateProgress();
        }
    },

    /**
     * Coleta dados do formulário
     */
    collectFormData() {
        const formData = {};

        // Step 1 - Dados do Cliente
        formData.cliente = document.getElementById('cliente')?.value || '';
        formData.telefone_cliente = Masks.unmaskPhone(document.getElementById('telefone_cliente')?.value || '');
        formData.destinatario = document.getElementById('destinatario')?.value || '';
        formData.tipo_pedido = document.querySelector('input[name="tipo_pedido"]:checked')?.value || 'Entrega';

        // Step 2 - Produto e Agendamento
        formData.produto = document.getElementById('produto')?.value || '';
        formData.flores_cor = document.getElementById('flores_cor')?.value || '';
        formData.valor = document.getElementById('valor')?.value || '';
        formData.dia_entrega = Masks.unmaskDate(document.getElementById('dia_entrega')?.value || '');
        formData.horario = Masks.unmaskTime(document.getElementById('horario')?.value || '');

        // Step 3 - Logística
        formData.endereco = document.getElementById('endereco')?.value || '';
        formData.obs_entrega = document.getElementById('obs_entrega')?.value || '';

        // Step 4 - Finalização
        formData.mensagem = document.getElementById('mensagem')?.value || '';
        formData.pagamento = document.getElementById('pagamento')?.value || '';
        formData.observacoes = document.getElementById('observacoes')?.value || '';

        return formData;
    },

    /**
     * Salva rascunho no localStorage
     */
    saveDraft() {
        const data = this.collectFormData();
        localStorage.setItem('form-draft', JSON.stringify(data));
        console.log('💾 Rascunho salvo');
    },

    /**
     * Carrega rascunho do localStorage
     */
    loadDraft() {
        const draft = localStorage.getItem('form-draft');
        
        if (draft) {
            try {
                const data = JSON.parse(draft);
                
                // Preencher campos
                Object.keys(data).forEach(key => {
                    const field = document.getElementById(key);
                    if (field) {
                        if (field.type === 'radio') {
                            const radio = document.querySelector(`input[name="${key}"][value="${data[key]}"]`);
                            if (radio) radio.checked = true;
                        } else {
                            field.value = data[key];
                        }
                    }
                });

                console.log('✅ Rascunho carregado');
                Notification.info('Rascunho anterior carregado');
            } catch (error) {
                console.error('Erro ao carregar rascunho:', error);
            }
        }
    },

    /**
     * Limpa rascunho
     */
    clearDraft() {
        localStorage.removeItem('form-draft');
        console.log('🗑️ Rascunho limpo');
    },

    /**
     * Submete formulário
     */
    async submitForm() {
        console.log('🚀 submitForm() CHAMADO!');
        console.log('Step atual:', this.currentStep);
        
        // Validar último step
        if (!this.validateCurrentStep()) {
            console.log('❌ Validação falhou');
            return;
        }

        console.log('✅ Validação OK! Coletando dados...');
        
        // Coletar dados
        const formData = this.collectFormData();
        console.log('📦 Dados coletados:', formData);

        // Validação final
        if (!formData.telefone_cliente || !formData.destinatario || !formData.produto || !formData.dia_entrega || !formData.horario) {
            Notification.error('Campos obrigatórios não preenchidos');
            return;
        }

        try {
            Utils.showLoading();

            // Se está offline, salvar no IndexedDB
            if (!Utils.isOnline()) {
                await DB.savePendingPedido(formData);
                
                Notification.success('Pedido salvo offline! Será sincronizado quando voltar online.');
                
                this.resetForm();
                Router.navigate('/painel');
                return;
            }

            // Enviar para API
            const result = await API.createPedido(formData);

            if (result.success) {
                Notification.success('Pedido criado com sucesso! 🎉');
                
                this.clearDraft();
                this.resetForm();
                
                // Navegar para o painel após 1 segundo
                setTimeout(() => {
                    Router.navigate('/painel');
                }, 1000);
            } else {
                throw new Error(result.error || 'Erro ao criar pedido');
            }

        } catch (error) {
            console.error('Erro ao enviar pedido:', error);
            Notification.error(`Erro ao criar pedido: ${error.message}`);
        } finally {
            Utils.hideLoading();
        }
    },

    /**
     * Reseta formulário
     */
    resetForm() {
        // Limpar todos os campos
        document.querySelectorAll('input, textarea, select').forEach(field => {
            if (field.type === 'radio' || field.type === 'checkbox') {
                field.checked = false;
            } else {
                field.value = '';
            }
            
            // Limpar validações visuais
            Validators.clearFieldError(field);
        });

        // Voltar para o primeiro step
        this.currentStep = 1;
        this.showStep(1);
        this.updateProgress();

        console.log('🔄 Formulário resetado');
    },

    /**
     * Preview dos dados antes de enviar
     */
    showPreview() {
        const data = this.collectFormData();

        const previewHtml = `
            <h2 class="text-2xl font-bold mb-4">Resumo do Pedido</h2>
            
            <div class="space-y-3 text-left">
                ${data.cliente ? `<p><strong>De:</strong> ${Utils.escapeHtml(data.cliente)}</p>` : ''}
                <p><strong>Telefone:</strong> ${Utils.formatPhone(data.telefone_cliente)}</p>
                <p><strong>Para:</strong> ${Utils.escapeHtml(data.destinatario)}</p>
                <p><strong>Tipo:</strong> ${Utils.translateType(data.tipo_pedido)}</p>
                <p><strong>Produto:</strong> ${Utils.escapeHtml(data.produto)}</p>
                ${data.flores_cor ? `<p><strong>Flores:</strong> ${Utils.escapeHtml(data.flores_cor)}</p>` : ''}
                ${data.valor ? `<p><strong>Valor:</strong> ${Utils.escapeHtml(data.valor)}</p>` : ''}
                <p><strong>Entrega:</strong> ${Utils.formatDate(data.dia_entrega)} às ${data.horario}</p>
                ${data.endereco ? `<p><strong>Endereço:</strong> ${Utils.escapeHtml(data.endereco)}</p>` : ''}
                ${data.mensagem ? `<p><strong>Mensagem:</strong> ${Utils.escapeHtml(data.mensagem)}</p>` : ''}
            </div>
        `;

        Modal.custom(previewHtml);
    }
};

