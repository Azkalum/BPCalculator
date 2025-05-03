class ConversaoBountyInicial:
    """
    Calcula o fator de conversão usando o stack inicial e o bounty inicial.
    """

    def __init__(self, stack_inicial, bounty_inicial_dolar):
        self.stack_inicial = stack_inicial
        self.bounty_inicial_dolar = bounty_inicial_dolar

    def calcular_fator_conversao(self):
        if self.bounty_inicial_dolar == 0:
            raise ValueError("O bounty inicial não pode ser zero!")
        return self.stack_inicial / self.bounty_inicial_dolar


class ConversaoBountyMedio:
    """
    Calcula o fator de conversão usando o stack médio e o bounty médio atuais do torneio.
    """

    def __init__(self, stack_medio, bounty_medio_dolar):
        self.stack_medio = stack_medio
        self.bounty_medio_dolar = bounty_medio_dolar

    def calcular_fator_conversao(self):
        if self.bounty_medio_dolar == 0:
            raise ValueError("O bounty médio não pode ser zero!")
        return self.stack_medio / self.bounty_medio_dolar


def limpar_entrada(valor):
    """
    Limpa a entrada do usuário:
    - Remove '$', 'R$', espaços.
    - Troca ',' por '.' para permitir vírgulas como separador decimal.
    """
    valor = valor.replace("$", "").replace("R$", "").strip()
    valor = valor.replace(",", ".")
    return valor


def calcular_equity_necessaria(stack_efetivo, bounty_dolar, fator_conversao, pot_atual, custo_call):
    """
    Calcula a equidade mínima necessária para dar call em um torneio PKO/KO.
    """
    bounty_em_fichas = bounty_dolar * fator_conversao
    pot_final = pot_atual + bounty_em_fichas
    equity_necessaria = custo_call / pot_final
    return bounty_em_fichas, pot_final, equity_necessaria * 100


def main():
    print("=== Calculadora de Bounty Power para PKO/KO ===\n")

    while True:
        # Pergunta qual tipo de cálculo de fator de conversão
        escolha = input("Deseja calcular o fator de conversão? (S/N): ").strip().lower()

        if escolha == 's':
            tipo = input("Deseja usar Stack Inicial (I) ou Stack Médio (M)? ").strip().lower()

            if tipo == 'i':
                try:
                    stack_inicial = float(limpar_entrada(input("Stack inicial do torneio (em fichas): ")))
                    bounty_inicial_dolar = float(limpar_entrada(input("Valor inicial do bounty (em dólares): ")))
                    conversao = ConversaoBountyInicial(stack_inicial, bounty_inicial_dolar)
                    fator_conversao = conversao.calcular_fator_conversao()
                    print(f"\n🔍 Fator de conversão (inicial) calculado: {fator_conversao:.2f} fichas por dólar.\n")
                except ValueError:
                    print("\n⚠️ Entrada inválida! Por favor, insira apenas números válidos.")
                    continue

            elif tipo == 'm':
                try:
                    stack_medio = float(limpar_entrada(input("Stack médio atual (em fichas): ")))
                    bounty_medio_dolar = float(limpar_entrada(input("Bounty médio atual (em dólares): ")))
                    conversao = ConversaoBountyMedio(stack_medio, bounty_medio_dolar)
                    fator_conversao = conversao.calcular_fator_conversao()
                    print(f"\n🔍 Fator de conversão (médio) calculado: {fator_conversao:.2f} fichas por dólar.\n")
                except ValueError:
                    print("\n⚠️ Entrada inválida! Por favor, insira apenas números válidos.")
                    continue

            else:
                print("\n⚠️ Opção inválida. Escolha 'I' para Inicial ou 'M' para Médio.")
                continue

        else:
            try:
                fator_conversao = float(limpar_entrada(input("Digite o fator de conversão manualmente: ")))
            except ValueError:
                print("\n⚠️ Entrada inválida! Por favor, insira apenas números válidos.")
                continue

        # Entrada de dados principais
        try:
            stack_efetivo = float(limpar_entrada(input("Stack efetivo (em fichas): ")))
            bounty_dolar = float(limpar_entrada(input("Valor do bounty (em dólares): ")))
            pot_atual = float(limpar_entrada(input("Pot atual antes do call (em fichas): ")))
            custo_call = float(limpar_entrada(input("Custo do seu call (em fichas): ")))
        except ValueError:
            print("\n⚠️ Entrada inválida! Por favor, insira apenas números válidos.")
            continue

        # Cálculo principal
        bounty_em_fichas, pot_final, equity_necessaria = calcular_equity_necessaria(
            stack_efetivo, bounty_dolar, fator_conversao, pot_atual, custo_call
        )

        # Resultados
        print("\n--- Resultados ---")
        print(f"Bounty convertido em fichas: {bounty_em_fichas:.2f}")
        print(f"Pot final (pot + bounty): {pot_final:.2f} fichas")
        print(f"Equidade mínima necessária para o call: {equity_necessaria:.2f}%")

        # Perguntar sua equidade atual no spot
        try:
            sua_equidade = float(limpar_entrada(
                input("\nDigite sua equidade no spot (em %, ex: 45.5) ou deixe em branco para pular: ") or 0))
            if sua_equidade > 0:
                if sua_equidade >= equity_necessaria:
                    print("✅ Recomendo: CALL!")
                else:
                    print("❌ Recomendo: FOLD.")
        except ValueError:
            print("⚠️ Equidade inválida! Pulando recomendação...")

        print("\n=========================")

        # Perguntar se deseja fazer novo cálculo
        novo = input("Deseja calcular outro spot? (S/N): ").strip().lower()
        if novo != 's':
            print("\nObrigado por usar a Calculadora de Bounty Power! 🎯 Boa sorte nas mesas! 🃏")
            break


if __name__ == "__main__":
    main()
