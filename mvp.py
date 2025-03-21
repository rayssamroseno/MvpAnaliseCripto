import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import csv

# Configuração do VADER (Análise de Sentimentos)
analyzer = SentimentIntensityAnalyzer()

# Criar a pasta "registros" para salvar gráficos e arquivos
os.makedirs("registros", exist_ok=True)

# Arquivos CSV para simular o banco de dados
decision_history_file = "decision_history.csv"

# Função para inicializar o arquivo CSV
def initialize_csv():
    if not os.path.exists(decision_history_file):
        with open(decision_history_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "symbol", "price", "quantity", "action", "timestamp"])
            print(f"Arquivo {decision_history_file} criado.")

# Função para salvar uma decisão no CSV
def save_decision_to_csv(history):
    with open(decision_history_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            history["name"],
            history["symbol"],
            history["price"],
            history["quantity"],
            history["action"],
            history["timestamp"]
        ])
        print(f"Decisão registrada no arquivo CSV: {history['name']} - {history['action']}")

# Função para carregar o histórico de decisões do CSV
def load_history_from_csv():
    if not os.path.exists(decision_history_file):
        return []
    with open(decision_history_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Função para buscar criptomoedas promissoras no CoinGecko
def fetch_promising_coins():
    print("Coletando dados do CoinGecko...")
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "brl",  # Preço em reais
        "order": "market_cap_desc",  # Ordenado pela maior capitalização
        "per_page": 50,  # Até 50 moedas por vez
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        promising_coins = []
        for coin in data:
            if 1 <= coin["current_price"] <= 100:  # Preço acessível
                sentiment = analyzer.polarity_scores(coin["name"])
                volume = coin["total_volume"]
                price_change = coin.get("price_change_percentage_24h", 0)

                # Lógica de recomendação aprimorada
                if sentiment["compound"] > 0.1 and volume > 50000 and price_change > 1:
                    recommendation = "Boa opção"
                    reason = "Alta positividade no sentimento, bom volume e tendência de alta."
                elif price_change < -1 and volume > 50000:
                    recommendation = "Observar"
                    reason = "Volume bom, mas tendência de queda; pode ser interessante monitorar."
                else:
                    recommendation = "Evite"
                    reason = "Sentimento negativo/neutro, volume baixo ou tendência desfavorável."

                record = {
                    "name": coin["name"],
                    "symbol": coin["symbol"],
                    "price": coin["current_price"],
                    "volume": volume,
                    "sentiment": sentiment,
                    "price_change_24h": price_change,
                    "recommendation": recommendation,
                    "reason": reason,
                    "source": "CoinGecko",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                promising_coins.append(record)
        return promising_coins
    else:
        print(f"Erro ao buscar criptomoedas do CoinGecko: {response.status_code}")
        return []

# Função para recomendar tempo para a próxima análise
def calculate_next_run_time(decision, coin_data):
    if decision == "Comprar":
        if float(coin_data["price_change_24h"]) > 5:
            return datetime.now() + timedelta(hours=1)
        elif float(coin_data["price_change_24h"]) > 0:
            return datetime.now() + timedelta(hours=3)
        else:
            return datetime.now() + timedelta(hours=6)
    elif decision == "Vender":
        return datetime.now() + timedelta(hours=2)
    elif decision == "Manter":
        return datetime.now() + timedelta(hours=4)
    else:
        return datetime.now() + timedelta(hours=5)

# Função para verificar o histórico e realizar ações com base nele
def view_history():
    print("\n=== HISTÓRICO DE DECISÕES ===")
    history = load_history_from_csv()
    if history:
        for record in history:
            print(f"Criptomoeda: {record['name']} - Ação: {record['action']} - "
                  f"Quantidade: {record['quantity']} - Preço: R${float(record['price']):.2f} - Data: {record['timestamp']}")

        while True:
            try:
                print("\nDeseja realizar alguma ação com base no histórico? (1 para Sim, 2 para Não)")
                action_choice = int(input("Digite sua escolha: "))
                if action_choice == 1:
                    print("\nEscolha uma criptomoeda do histórico para realizar uma ação:")
                    for i, record in enumerate(history, 1):
                        print(f"{i}. {record['name']} - Última ação: {record['action']} - Quantidade: {record['quantity']}")
                    choice = int(input("Digite o número da criptomoeda escolhida ou 0 para sair: ")) - 1

                    if 0 <= choice < len(history):
                        selected_record = history[choice]
                        print("\nDecisões disponíveis:")
                        print("1. Comprar mais")
                        print("2. Vender")
                        print("3. Manter")
                        action = int(input("Digite sua escolha (1, 2, 3) ou 0 para sair: "))
                        if action == 0:
                            return
                        action_str = "Comprar mais" if action == 1 else "Vender" if action == 2 else "Manter"

                        # Perguntar quantidade
                        quantity = float(input("Digite a quantidade para esta ação: "))
                        current_quantity = float(selected_record.get("quantity", 0))

                        if action_str == "Comprar mais":
                            current_quantity += quantity
                        elif action_str == "Vender":
                            current_quantity -= quantity

                        # Atualizar o histórico com a nova quantidade
                        updated_history = {
                            "name": selected_record["name"],
                            "symbol": selected_record["symbol"],
                            "price": float(selected_record["price"]),
                            "quantity": current_quantity,
                            "action": action_str,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_decision_to_csv(updated_history)
                        print(f"Ação registrada: {selected_record['name']} - {action_str} - Quantidade: {quantity}")
                    else:
                        print("Escolha inválida. Retornando ao menu principal.")
                        break
                elif action_choice == 2:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    else:
        print("Nenhuma decisão registrada no histórico.")

# Função para registrar decisão e oferecer opção de continuar
def register_decision_and_rerun(data):
    while True:
        try:
            print("\n=== RECOMENDAÇÕES ===")
            for i, item in enumerate(data, 1):
                print(f"{i}. {item['name']} (Símbolo: {item['symbol']}) - Preço: R${item['price']:.2f} - "
                      f"Recomendação: {item['recommendation']}")

            print("\nEscolha uma criptomoeda para registrar sua decisão (1, 2, 3, ...) ou 0 para sair:")
            choice = int(input("Digite o número da criptomoeda escolhida: ")) - 1

            if choice == -1:
                print("Saindo sem registrar decisão.")
                return

            if 0 <= choice < len(data):
                selected_coin = data[choice]
                print("\nDecisões disponíveis:")
                print("1. Comprar")
                print("2. Vender")
                print("3. Manter")
                action = int(input("Digite sua escolha (1, 2, 3) ou 0 para sair: "))
                if action == 0:
                    return
                action_str = "Comprar" if action == 1 else "Vender" if action == 2 else "Manter"

                # Perguntar quantidade
                quantity = float(input("Digite a quantidade para esta ação: "))

                # Salvar decisão no histórico
                history = {
                    "name": selected_coin["name"],
                    "symbol": selected_coin["symbol"],
                    "price": selected_coin["price"],
                    "quantity": quantity,
                    "action": action_str,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_decision_to_csv(history)
                print(f"Decisão registrada: {selected_coin['name']} - {action_str} - Quantidade: {quantity}")

                # Calcular tempo para próxima análise
                next_run_time = calculate_next_run_time(action_str, selected_coin)
                print(f"\nRecomenda-se rodar o programa novamente em: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Perguntar ao usuário se deseja continuar
                print("\nDeseja continuar? (1 para Sim, 2 para Não)")
                continue_choice = int(input("Digite sua escolha: "))
                if continue_choice == 1:
                    print("\nRodando nova análise com base na decisão anterior...")
                    run_mvp()
                else:
                    print("Encerrando o programa. Histórico salvo.")
                    return
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

# Função para rodar o MVP
def run_mvp():
    initialize_csv()  # Inicializar CSV caso não exista
    print("Iniciando o MVP...")
    print("\nDeseja visualizar o histórico antes de continuar? (1 para Sim, 2 para Não)")
    while True:
        try:
            view_choice = int(input("Digite sua escolha: "))
            if view_choice == 1:
                view_history()
                break
            elif view_choice == 2:
                break
            else:
                print("Opção inválida. Digite 1 ou 2.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    promising_coins = fetch_promising_coins()
    if promising_coins:
        register_decision_and_rerun(promising_coins)
    else:
        print("Nenhuma criptomoeda promissora encontrada.")

if __name__ == "__main__":
    run_mvp()
