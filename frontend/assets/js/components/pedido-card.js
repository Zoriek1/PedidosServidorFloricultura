/**
 * Plante Uma Flor - PWA v3.0
 * Pedido Card Component - Card de pedido para o painel
 */

const PedidoCard = {
    /**
     * Cria HTML de um card de pedido
     */
    create(pedido) {
        const card = document.createElement('div');
        card.className = `pedido-card status-${pedido.status}`;
        card.dataset.id = pedido.id;
        card.dataset.status = pedido.status;

        // Verificar se o pedido está atrasado
        const isOverdue = this.isOverdue(pedido);
        const overdueClass = isOverdue ? 'text-red-600 font-bold' : '';

        card.innerHTML = `
            <div class="flex justify-between items-start mb-3">
                <div class="flex-1">
                    <h3 class="text-lg font-bold text-gray-800">
                        Pedido #${pedido.id}
                    </h3>
                    <p class="text-sm text-gray-600">
                        <i class="fas fa-calendar mr-1"></i>
                        ${Utils.formatDate(pedido.dia_entrega)} às ${pedido.horario}
                        ${isOverdue ? '<span class="text-red-600 ml-2"><i class="fas fa-exclamation-triangle"></i> Atrasado</span>' : ''}
                    </p>
                </div>
                <span class="status-badge status-${pedido.status}">
                    ${Utils.translateStatus(pedido.status)}
                </span>
            </div>

            <div class="space-y-2 mb-4">
                ${pedido.cliente ? `
                    <p class="text-sm">
                        <i class="fas fa-user text-gray-400 w-5"></i>
                        <strong>De:</strong> ${Utils.escapeHtml(pedido.cliente)}
                    </p>
                ` : ''}
                
                <p class="text-sm">
                    <i class="fas fa-gift text-gray-400 w-5"></i>
                    <strong>Para:</strong> ${Utils.escapeHtml(pedido.destinatario)}
                </p>

                ${pedido.telefone_cliente ? `
                    <p class="text-sm">
                        <i class="fas fa-phone text-gray-400 w-5"></i>
                        ${Utils.formatPhone(pedido.telefone_cliente)}
                    </p>
                ` : ''}

                <p class="text-sm">
                    <i class="fas fa-flower text-gray-400 w-5"></i>
                    ${Utils.escapeHtml(Utils.truncate(pedido.produto, 60))}
                </p>

                ${pedido.tipo_pedido ? `
                    <p class="text-sm">
                        <i class="fas ${pedido.tipo_pedido === 'Entrega' ? 'fa-truck' : 'fa-store'} text-gray-400 w-5"></i>
                        ${Utils.translateType(pedido.tipo_pedido)}
                    </p>
                ` : ''}

                ${pedido.endereco && pedido.tipo_pedido === 'Entrega' ? `
                    <p class="text-sm">
                        <i class="fas fa-map-marker-alt text-gray-400 w-5"></i>
                        ${Utils.escapeHtml(Utils.truncate(pedido.endereco, 60))}
                    </p>
                ` : ''}

                ${pedido.valor ? `
                    <p class="text-sm">
                        <i class="fas fa-dollar-sign text-gray-400 w-5"></i>
                        ${Utils.escapeHtml(pedido.valor)}
                    </p>
                ` : ''}
            </div>

            <div class="flex gap-2 pt-3 border-t border-gray-200">
                <select 
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-primary"
                    onchange="PainelManager.changeStatus(${pedido.id}, this.value)"
                >
                    <option value="">Alterar Status</option>
                    <option value="agendado" ${pedido.status === 'agendado' ? 'selected' : ''}>Agendado</option>
                    <option value="em_producao" ${pedido.status === 'em_producao' ? 'selected' : ''}>Em Produção</option>
                    <option value="pronto_entrega" ${pedido.status === 'pronto_entrega' ? 'selected' : ''}>Pronto para Entrega</option>
                    <option value="em_rota" ${pedido.status === 'em_rota' ? 'selected' : ''}>Em Rota</option>
                    <option value="pronto_retirada" ${pedido.status === 'pronto_retirada' ? 'selected' : ''}>Pronto para Retirada</option>
                    <option value="concluido" ${pedido.status === 'concluido' ? 'selected' : ''}>Concluído</option>
                </select>

                <button 
                    class="px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
                    onclick="PedidoCard.printPedido(${pedido.id})"
                    title="Imprimir Pedido"
                >
                    <i class="fas fa-print"></i>
                </button>

                <button 
                    class="px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
                    onclick="PedidoCard.showDetails(${pedido.id})"
                    title="Ver detalhes"
                >
                    <i class="fas fa-eye"></i>
                </button>

                <button 
                    class="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
                    onclick="PainelManager.deletePedido(${pedido.id})"
                    title="Deletar pedido"
                >
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return card;
    },

    /**
     * Verifica se pedido está atrasado
     */
    isOverdue(pedido) {
        if (pedido.status === 'concluido') {
            return false;
        }

        try {
            const now = new Date();
            const deliveryDate = new Date(pedido.dia_entrega + 'T' + pedido.horario);
            return now > deliveryDate;
        } catch (error) {
            return false;
        }
    },

    /**
     * Mostra detalhes completos do pedido
     */
    async showDetails(pedidoId) {
        try {
            Utils.showLoading();
            
            const result = await API.getPedido(pedidoId);
            
            if (!result.success) {
                throw new Error(result.error || 'Erro ao carregar pedido');
            }

            const pedido = result.data.pedido;

            const modalContent = `
                <div class="max-h-[80vh] overflow-y-auto">
                    <div class="flex justify-between items-start mb-4">
                        <h2 class="text-2xl font-bold text-gray-800">
                            Pedido #${pedido.id}
                        </h2>
                        <button data-modal-close class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times text-2xl"></i>
                        </button>
                    </div>

                    <div class="space-y-4">
                        <!-- Status -->
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <span class="status-badge status-${pedido.status}">
                                ${Utils.translateStatus(pedido.status)}
                            </span>
                        </div>

                        <!-- Cliente -->
                        ${pedido.cliente ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">De (Remetente):</h3>
                                <p class="text-gray-800">${Utils.escapeHtml(pedido.cliente)}</p>
                            </div>
                        ` : ''}

                        <!-- Telefone -->
                        ${pedido.telefone_cliente ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Telefone:</h3>
                                <p class="text-gray-800">${Utils.formatPhone(pedido.telefone_cliente)}</p>
                            </div>
                        ` : ''}

                        <!-- Destinatário -->
                        <div>
                            <h3 class="font-semibold text-gray-700 mb-1">Para (Destinatário):</h3>
                            <p class="text-gray-800 font-bold">${Utils.escapeHtml(pedido.destinatario)}</p>
                        </div>

                        <!-- Tipo -->
                        ${pedido.tipo_pedido ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Tipo:</h3>
                                <p class="text-gray-800">${Utils.translateType(pedido.tipo_pedido)}</p>
                            </div>
                        ` : ''}

                        <!-- Produto -->
                        <div>
                            <h3 class="font-semibold text-gray-700 mb-1">Produto:</h3>
                            <p class="text-gray-800 whitespace-pre-wrap">${Utils.escapeHtml(pedido.produto)}</p>
                        </div>

                        <!-- Flores e Cor -->
                        ${pedido.flores_cor ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Flores e Cor:</h3>
                                <p class="text-gray-800 whitespace-pre-wrap">${Utils.escapeHtml(pedido.flores_cor)}</p>
                            </div>
                        ` : ''}

                        <!-- Valor -->
                        ${pedido.valor ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Valor:</h3>
                                <p class="text-gray-800 text-xl font-bold text-green-600">${Utils.escapeHtml(pedido.valor)}</p>
                            </div>
                        ` : ''}

                        <!-- Data e Horário -->
                        <div class="bg-blue-50 p-4 rounded-lg">
                            <h3 class="font-semibold text-gray-700 mb-2">Entrega:</h3>
                            <p class="text-gray-800">
                                <i class="fas fa-calendar mr-2"></i>
                                ${Utils.formatDate(pedido.dia_entrega)}
                            </p>
                            <p class="text-gray-800">
                                <i class="fas fa-clock mr-2"></i>
                                ${pedido.horario}
                            </p>
                        </div>

                        <!-- Endereço -->
                        ${pedido.endereco ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Endereço:</h3>
                                <p class="text-gray-800 whitespace-pre-wrap">${Utils.escapeHtml(pedido.endereco)}</p>
                            </div>
                        ` : ''}

                        <!-- Observações de Entrega -->
                        ${pedido.obs_entrega ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Como Entregar:</h3>
                                <p class="text-gray-800 whitespace-pre-wrap">${Utils.escapeHtml(pedido.obs_entrega)}</p>
                            </div>
                        ` : ''}

                        <!-- Mensagem -->
                        ${pedido.mensagem ? `
                            <div class="bg-pink-50 p-4 rounded-lg">
                                <h3 class="font-semibold text-gray-700 mb-1">Carta/Mensagem:</h3>
                                <p class="text-gray-800 whitespace-pre-wrap italic">${Utils.escapeHtml(pedido.mensagem)}</p>
                            </div>
                        ` : ''}

                        <!-- Pagamento -->
                        ${pedido.pagamento ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Forma de Pagamento:</h3>
                                <p class="text-gray-800">${Utils.escapeHtml(pedido.pagamento)}</p>
                            </div>
                        ` : ''}

                        <!-- Observações -->
                        ${pedido.observacoes ? `
                            <div>
                                <h3 class="font-semibold text-gray-700 mb-1">Observações Gerais:</h3>
                                <p class="text-gray-800 whitespace-pre-wrap">${Utils.escapeHtml(pedido.observacoes)}</p>
                            </div>
                        ` : ''}

                        <!-- Informações de Sistema -->
                        <div class="text-xs text-gray-500 pt-4 border-t">
                            <p>Criado em: ${pedido.created_at}</p>
                            ${pedido.updated_at ? `<p>Atualizado em: ${pedido.updated_at}</p>` : ''}
                        </div>
                    </div>
                </div>
            `;

            Modal.custom(modalContent);

        } catch (error) {
            console.error('Erro ao carregar detalhes:', error);
            Notification.error('Erro ao carregar detalhes do pedido');
        } finally {
            Utils.hideLoading();
        }
    },

    /**
     * Imprime pedido em formato A4
     */
    async printPedido(pedidoId) {
        try {
            Utils.showLoading();
            
            const result = await API.getPedido(pedidoId);
            
            if (!result.success) {
                throw new Error(result.error || 'Erro ao carregar pedido');
            }

            const pedido = result.data.pedido;

            // Criar janela de impressão
            const printWindow = window.open('', '_blank', 'width=800,height=600');
            
            if (!printWindow) {
                Notification.error('Popup bloqueado! Permita popups para imprimir.');
                return;
            }

            // HTML para impressão em A4
            const printHTML = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pedido #${pedido.id} - Plante Uma Flor</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            border-bottom: 3px solid #9333ea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #9333ea;
            font-size: 28pt;
            margin-bottom: 5px;
        }
        
        .header p {
            color: #666;
            font-size: 11pt;
        }
        
        .pedido-numero {
            background: #9333ea;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            font-weight: bold;
            font-size: 16pt;
            margin: 20px 0;
        }
        
        .section {
            margin-bottom: 25px;
            page-break-inside: avoid;
        }
        
        .section-title {
            background: #f3f4f6;
            padding: 8px 12px;
            border-left: 4px solid #9333ea;
            font-weight: bold;
            font-size: 14pt;
            margin-bottom: 10px;
        }
        
        .field {
            margin-bottom: 12px;
            padding-left: 10px;
        }
        
        .field-label {
            font-weight: bold;
            color: #555;
            display: inline-block;
            min-width: 150px;
        }
        
        .field-value {
            color: #333;
        }
        
        .field-value.highlight {
            color: #9333ea;
            font-weight: bold;
            font-size: 14pt;
        }
        
        .message-box {
            background: #fef3c7;
            border: 2px solid #f59e0b;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-style: italic;
        }
        
        .delivery-box {
            background: #dbeafe;
            border: 2px solid #3b82f6;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            text-align: center;
            color: #666;
            font-size: 10pt;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 11pt;
        }
        
        .status-agendado { background: #e5e7eb; color: #374151; }
        .status-em_producao { background: #fef3c7; color: #92400e; }
        .status-pronto_entrega, .status-pronto_retirada { background: #d1fae5; color: #065f46; }
        .status-em_rota { background: #dbeafe; color: #1e40af; }
        .status-concluido { background: #d1fae5; color: #166534; }
        
        @media print {
            body {
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }
            
            .no-print {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Cabeçalho -->
        <div class="header">
            <h1>🌺 Plante Uma Flor</h1>
            <p>Sistema de Gestão de Pedidos</p>
        </div>

        <!-- Número do Pedido -->
        <div style="text-align: center;">
            <div class="pedido-numero">
                PEDIDO #${pedido.id}
            </div>
            <p style="margin-top: 10px;">
                <span class="status-badge status-${pedido.status}">
                    ${Utils.translateStatus(pedido.status).toUpperCase()}
                </span>
            </p>
        </div>

        <!-- Informações do Cliente -->
        <div class="section">
            <div class="section-title">👤 Informações do Cliente</div>
            ${pedido.cliente ? `
                <div class="field">
                    <span class="field-label">De (Remetente):</span>
                    <span class="field-value">${pedido.cliente}</span>
                </div>
            ` : ''}
            <div class="field">
                <span class="field-label">Telefone:</span>
                <span class="field-value">${Utils.formatPhone(pedido.telefone_cliente)}</span>
            </div>
            <div class="field">
                <span class="field-label">Para (Destinatário):</span>
                <span class="field-value highlight">${pedido.destinatario}</span>
            </div>
            <div class="field">
                <span class="field-label">Tipo de Pedido:</span>
                <span class="field-value">${Utils.translateType(pedido.tipo_pedido)}</span>
            </div>
        </div>

        <!-- Produto -->
        <div class="section">
            <div class="section-title">🌸 Produto</div>
            <div class="field">
                <span class="field-label">Produto:</span>
                <div class="field-value" style="margin-top: 5px; white-space: pre-wrap;">${pedido.produto}</div>
            </div>
            ${pedido.flores_cor ? `
                <div class="field">
                    <span class="field-label">Flores e Cor:</span>
                    <div class="field-value" style="margin-top: 5px; white-space: pre-wrap;">${pedido.flores_cor}</div>
                </div>
            ` : ''}
            ${pedido.valor ? `
                <div class="field">
                    <span class="field-label">Valor:</span>
                    <span class="field-value" style="font-size: 16pt; color: #059669; font-weight: bold;">${pedido.valor}</span>
                </div>
            ` : ''}
        </div>

        <!-- Data e Horário -->
        <div class="section">
            <div class="delivery-box">
                <div style="font-weight: bold; font-size: 14pt; margin-bottom: 10px;">
                    📅 Entrega Agendada
                </div>
                <div class="field">
                    <span class="field-label">Data:</span>
                    <span class="field-value highlight">${Utils.formatDate(pedido.dia_entrega)}</span>
                </div>
                <div class="field">
                    <span class="field-label">Horário:</span>
                    <span class="field-value highlight">${pedido.horario}</span>
                </div>
            </div>
        </div>

        <!-- Endereço -->
        ${pedido.endereco ? `
            <div class="section">
                <div class="section-title">📍 Endereço de Entrega</div>
                <div class="field">
                    <div class="field-value" style="white-space: pre-wrap;">${pedido.endereco}</div>
                </div>
                ${pedido.obs_entrega ? `
                    <div class="field" style="margin-top: 10px;">
                        <span class="field-label">Observações:</span>
                        <div class="field-value" style="margin-top: 5px; white-space: pre-wrap;">${pedido.obs_entrega}</div>
                    </div>
                ` : ''}
            </div>
        ` : ''}

        <!-- Mensagem -->
        ${pedido.mensagem ? `
            <div class="section">
                <div class="section-title">💌 Carta/Mensagem</div>
                <div class="message-box">
                    ${pedido.mensagem.replace(/\n/g, '<br>')}
                </div>
            </div>
        ` : ''}

        <!-- Pagamento -->
        ${pedido.pagamento ? `
            <div class="section">
                <div class="section-title">💳 Pagamento</div>
                <div class="field">
                    <span class="field-label">Forma de Pagamento:</span>
                    <span class="field-value">${pedido.pagamento}</span>
                </div>
            </div>
        ` : ''}

        <!-- Observações Gerais -->
        ${pedido.observacoes ? `
            <div class="section">
                <div class="section-title">📝 Observações Gerais</div>
                <div class="field">
                    <div class="field-value" style="white-space: pre-wrap;">${pedido.observacoes}</div>
                </div>
            </div>
        ` : ''}

        <!-- Rodapé -->
        <div class="footer">
            <p>Impresso em: ${new Date().toLocaleString('pt-BR')}</p>
            <p style="margin-top: 5px;">Plante Uma Flor - Sistema de Gestão de Pedidos v3.0</p>
        </div>

        <!-- Botão de Impressão (esconde ao imprimir) -->
        <div class="no-print" style="text-align: center; margin-top: 30px;">
            <button onclick="window.print()" style="
                background: #9333ea;
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 14pt;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
            ">
                🖨️ Imprimir Pedido
            </button>
            <button onclick="window.close()" style="
                background: #6b7280;
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 14pt;
                border-radius: 8px;
                cursor: pointer;
                margin-left: 10px;
            ">
                ✕ Fechar
            </button>
        </div>
    </div>

    <script>
        // Auto-imprimir após carregar (opcional)
        // window.onload = () => window.print();
    </script>
</body>
</html>
            `;

            printWindow.document.write(printHTML);
            printWindow.document.close();

            Notification.success('Janela de impressão aberta!');

        } catch (error) {
            console.error('Erro ao imprimir pedido:', error);
            Notification.error('Erro ao gerar impressão do pedido');
        } finally {
            Utils.hideLoading();
        }
    }
};

