# Gerador de Pedidos — Plante Uma Flor

Sistema para geração de PDFs de pedidos para floricultura com armazenamento em banco de dados SQLite.

## Funcionalidades

- Interface gráfica intuitiva com formulário em 3 etapas
- Geração automática de PDFs de pedidos
- Armazenamento em banco de dados SQLite
- Exportação de dados para CSV
- Validação de datas e horários
- Formatação automática de valores monetários

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python (ver `requirements.txt`)

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd Gerador-BC-Pedidos-Floricultura
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o aplicativo:
```bash
python PDFgen.py
```

Ou execute o executável buildado:
```bash
dist/PDFgen.exe
```

## Estrutura de Dados

Os pedidos são armazenados automaticamente em `pedidos.db` na pasta de saída configurada (padrão: `Documents/Pedidos-Floricultura`).

### Campos do Pedido

- **Cliente**: Quem envia o pedido
- **Destinatário**: Pessoa que receberá o pedido (obrigatório)
- **Produto**: Descrição do produto
- **Valor**: Valor total do pedido
- **Endereço**: Endereço completo de entrega
- **Data de Entrega**: Formato DD/MM/YYYY
- **Horário**: Formato HH:MM
- **Observações**: Como entregar
- **Mensagem**: Mensagem do cartão
- **Pagamento**: Forma de pagamento

## Build

Para criar um executável standalone:

```bash
pip install pyinstaller
pyinstaller PDFgen.spec
```

O executável será gerado em `dist/PDFgen.exe`

## Licença

Este projeto é para uso interno da Plante Uma Flor Floricultura.

## Autor

Desenvolvido para auxiliar na gestão de pedidos da floricultura.

