# 🎨 Estilo iFood - Painel de Pedidos

## 📋 Visão Geral

Foi criado um novo arquivo CSS (`style_ifood.css`) que replica o design do painel iFood para o sistema de gerenciamento de pedidos da Plante Uma Flor.

### Características Principais

✅ **Cores iFood**: Vermelho (#EA1D2C) e laranja (#FF6900)  
✅ **Layout Moderno**: Cards com sombras suaves  
✅ **Hierarquia Visual**: Tipografia clara e hierarquizada  
✅ **Badges Coloridos**: Status com cores distintas  
✅ **Hover Effects**: Transições suaves nos botões  
✅ **Totalmente Responsivo**: Adaptável a qualquer tela  

---

## 🎨 Cores Utilizadas

### Paleta Principal
- **Vermelho iFood**: `#EA1D2C`
- **Laranja**: `#FF6900`
- **Vermelho Escuro**: `#C41620`

### Paleta Neutra
- **Fundo Claro**: `#F5F5F5`
- **Fundo Branco**: `#FFFFFF`
- **Texto Escuro**: `#1A1A1A`
- **Texto Cinza**: `#6E6E6E`

### Cores de Status
- **Verde (Concluído)**: `#00D4AA`
- **Amarelo (Pendente)**: `#FFC107`
- **Azul (Em Produção)**: `#2196F3`
- **Cinza**: `#E0E0E0`

---

## 📁 Arquivos

### Criados
1. **`style_ifood.css`** - Estilo completo estilo iFood
2. **`painel_ifood.html`** - Template HTML com novo estilo
3. **`ESTILO_IFOOD_README.md`** - Este arquivo

---

## 🚀 Como Aplicar o Novo Estilo

### Opção 1: Usar o Novo Template

Edite `Servidor/static/app.py` na função `index()`:

```python
@app.route('/')
def index():
    """Página principal com listagem de pedidos"""
    try:
        pedidos = Pedido.query.order_by(Pedido.created_at.desc()).all()
        return render_template('painel_ifood.html', pedidos=pedidos)  # ← Trocar aqui
    except Exception as e:
        print(f"Erro ao buscar pedidos: {e}")
        return render_template('painel_ifood.html', pedidos=[])  # ← E aqui
```

### Opção 2: Substituir o CSS Atual

1. Renomeie `style.css` para `style.css.old`
2. Renomeie `style_ifood.css` para `style.css`
3. Ou simplesmente troque a referência no HTML

### Opção 3: Criar uma Rota Separada

```python
@app.route('/painel-ifood')
def painel_ifood():
    """Painel com estilo iFood"""
    try:
        pedidos = Pedido.query.order_by(Pedido.created_at.desc()).all()
        return render_template('painel_ifood.html', pedidos=pedidos)
    except Exception as e:
        print(f"Erro ao buscar pedidos: {e}")
        return render_template('painel_ifood.html', pedidos=[])
```

---

## 🎯 Comparação de Estilos

### Antigo (Arquivo: `style.css`)
- Background com gradiente roxo
- Cards com bordas azuis
- Cores mais tradicionais
- Design mais "corporativo"

### Novo (Arquivo: `style_ifood.css`)
- Background cinza claro
- Cards com bordas coloridas por status
- Cores vibrantes (vermelho iFood)
- Design mais moderno e intuitivo

---

## 📐 Estrutura do Layout

### Desktop (> 1024px)
```
┌─────────────────────────────────┐
│         HEADER                  │
├─────────────────────────────────┤
│  STATS (4 cards lado a lado)   │
├─────────────────────────────────┤
│  PEDIDOS (grid 3-4 colunas)     │
│  [Card] [Card] [Card]          │
│  [Card] [Card] [Card]          │
└─────────────────────────────────┘
```

### Tablet (768px - 1024px)
```
┌────────────────────────┐
│      HEADER            │
├────────────────────────┤
│  STATS (2 colunas)    │
│  [Stat] [Stat]        │
│  [Stat] [Stat]        │
├────────────────────────┤
│  PEDIDOS (2 colunas)  │
│  [Card] [Card]        │
│  [Card] [Card]       │
└────────────────────────┘
```

### Mobile (< 768px)
```
┌───────────┐
│  HEADER   │
├───────────┤
│  STATS    │
│  [Stat]   │
│  [Stat]   │
│  [Stat]   │
│  [Stat]   │
├───────────┤
│  PEDIDOS  │
│  [Card]   │
│  [Card]   │
│  [Card]   │
└───────────┘
```

---

## 🎨 Componentes Visuais

### 1. Cards de Pedidos

```css
.pedido-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border-left: 4px solid [COR DO STATUS];
}
```

**Cores de borda por status:**
- Pendente: Amarelo (#FFC107)
- Em Produção: Azul (#2196F3)
- Concluído: Verde (#00D4AA)

### 2. Botões

```css
.btn-primary {
    background: #EA1D2C;  /* Vermelho iFood */
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
}
```

**Hover Effect:**
```css
.btn-primary:hover {
    background: #C41620;  /* Vermelho mais escuro */
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
```

### 3. Badges de Status

```css
.badge-pendente {
    background: #FFF3CD;
    color: #F57C00;
}

.badge-em_producao {
    background: #E3F2FD;
    color: #1976D2;
}

.badge-concluido {
    background: #E0F2F1;
    color: #00796B;
}
```

### 4. Stats Cards

```css
.stat-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #EA1D2C;  /* Vermelho iFood */
}
```

---

## 📱 Responsividade

### Breakpoints

```css
@media (max-width: 1400px) {
    .pedidos-grid {
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    }
}

@media (max-width: 1024px) {
    .pedidos-grid {
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 16px;
    }
}

@media (max-width: 768px) {
    .pedidos-grid {
        grid-template-columns: 1fr;
    }
}
```

---

## 🎯 Melhorias Implementadas

1. ✅ **Tipografia Hierárquica**
   - Títulos grandes e em negrito
   - Labels menores e em cinza
   - Destaque para números (stats)

2. ✅ **Espaçamento Consistente**
   - Padding e margin uniformes
   - Gaps adequados entre elementos

3. ✅ **Cores Vibrantes**
   - Vermelho iFood para ações principais
   - Cores distintas para cada status
   - Backgrounds neutros para descanso visual

4. ✅ **Hover Effects Suaves**
   - Todos os cards têm hover
   - Botões com transições
   - Feedback visual claro

5. ✅ **Badges com Contadores**
   - Visualização rápida de quantidade
   - Cores identificam status
   - Formato arredondado

---

## 🚀 Como Testar

1. **Substitua o CSS atual** (seguindo opções acima)
2. **Reinicie o servidor Flask**
3. **Acesse:** http://localhost:5000
4. **Verifique:** Visual deve estar no estilo iFood

---

## 📊 Resultado Final

O painel agora possui:
- ✅ Visual moderno e profissional
- ✅ Layout limpo e organizado
- ✅ Cores vibrantes (vermelho iFood)
- ✅ Totalmente responsivo
- ✅ Experiência de usuário intuitiva

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

