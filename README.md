# MVP de Análise de Criptomoedas

Este projeto é um MVP (Minimum Viable Product) para análise e recomendação de criptomoedas com base em dados de mercado e sentimentos. Ele utiliza a API do CoinGecko para coletar dados de criptomoedas e a biblioteca VADER para análise de sentimentos. O objetivo é fornecer recomendações de compra, venda ou manutenção de criptomoedas com base em critérios como preço, volume e mudança percentual no preço.

## Funcionalidades

- Coleta de dados de criptomoedas em tempo real via API do CoinGecko.
- Análise de sentimentos usando a biblioteca VADER.
- Recomendações de ações (Comprar, Vender, Manter) com base em critérios predefinidos.
- Registro de decisões em um arquivo CSV para histórico.
- Visualização do histórico de decisões e possibilidade de realizar novas ações com base nele.

## Pré-requisitos

- Python 3.7 ou superior.
- Bibliotecas Python: `requests`, `vaderSentiment`, `matplotlib`.

## Configuração do Ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/rayssamroseno/MvpAnaliseCripto.git
   cd MvpAnaliseCripto
      ```

2. **Instale as dependências:**

```bash
pip install requests vaderSentiment matplotlib
```

3. **Execute o script principal:**

```bash
python mvp.py
```

4. **Siga as instruções no terminal:**

O programa irá coletar dados de criptomoedas e fornecer recomendações.

Você poderá registrar decisões de compra, venda ou manutenção.

O histórico de decisões será salvo no arquivo decision_history.csv.

## Estrutura do Projeto

mvp.py: Script principal que contém a lógica de coleta de dados, análise e recomendação. Este arquivo é obrigatório.

decision_history.csv: Arquivo CSV que armazena o histórico de decisões. Ele é criado automaticamente, mas você pode incluí-lo no repositório como exemplo. É opcional, mas útil.

## Contribuição

Contribuições são bem-vindas! Se você quiser contribuir para o projeto, siga os passos abaixo:

Faça um fork do repositório.

Crie uma branch para sua feature (git checkout -b feature/nova-feature).

Commit suas mudanças (git commit -m 'Adicionando nova feature').

Push para a branch (git push origin feature/nova-feature).

Abra um Pull Request.

