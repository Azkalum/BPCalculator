import streamlit as st

# Funções auxiliares
def limpar_entrada(valor):
    valor = str(valor).replace("$", "").replace("R$", "").strip().replace(",", ".")
    return float(valor)

def calcular_fator_conversao(stack, bounty):
    if bounty == 0:
        raise ValueError("O bounty não pode ser zero!")
    return stack / bounty

def calcular_equity_necessaria(stack_efetivo, bounty_dolar, fator_conversao, pot_atual, custo_call):
    bounty_em_fichas = bounty_dolar * fator_conversao
    pot_final = pot_atual + bounty_em_fichas
    equity_necessaria = custo_call / pot_final
    return bounty_em_fichas, pot_final, equity_necessaria * 100


# Título do App
st.set_page_config(page_title="Calculadora de Bounty Power", layout="centered")
st.title("📊 Calculadora de Bounty Power para PKO/KO")

# Escolha do tipo de fator de conversão
tipo = st.radio("Como deseja calcular o fator de conversão?", ["Stack Inicial", "Stack Médio", "Manual"])

try:
    if tipo == "Manual":
        fator_conversao = limpar_entrada(st.text_input("Fator de conversão manual (fichas por $1):", value="2000"))
    else:
        stack = limpar_entrada(st.text_input(f"{tipo} (fichas):", value="50000"))
        bounty = limpar_entrada(st.text_input(f"Bounty {'inicial' if tipo == 'Stack Inicial' else 'médio'} (em $):", value="25"))
        fator_conversao = calcular_fator_conversao(stack, bounty)
        st.success(f"Fator de conversão calculado: {fator_conversao:.2f} fichas por $1")

    # Entradas principais
    stack_efetivo = limpar_entrada(st.text_input("Stack efetivo (fichas):", value="40000"))
    bounty_dolar = limpar_entrada(st.text_input("Bounty do vilão (em $):", value="15"))
    pot_atual = limpar_entrada(st.text_input("Pot atual antes do call (fichas):", value="25000"))
    custo_call = limpar_entrada(st.text_input("Custo do call (fichas):", value="20000"))
    sua_equidade = st.text_input("Sua equidade no spot (% - opcional):", value="")

    # Botão de cálculo
    if st.button("Calcular"):
        bounty_em_fichas, pot_final, equity_necessaria = calcular_equity_necessaria(
            stack_efetivo, bounty_dolar, fator_conversao, pot_atual, custo_call
        )

        st.subheader("📈 Resultados")
        st.write(f"- Bounty convertido em fichas: **{bounty_em_fichas:.2f}**")
        st.write(f"- Pot final (pot + bounty): **{pot_final:.2f} fichas**")
        st.write(f"- Equidade mínima necessária para dar o call: **{equity_necessaria:.2f}%**")

        # Se ele informar a equidade
        if sua_equidade.strip() != "":
            try:
                equidade_real = float(limpar_entrada(sua_equidade))
                if equidade_real >= equity_necessaria:
                    st.success("✅ Recomendo: CALL!")
                else:
                    st.error("❌ Recomendo: FOLD.")
            except:
                st.warning("Equidade inválida. Use apenas números como 45.5")
except Exception as e:
    st.error(f"Erro: {e}")
