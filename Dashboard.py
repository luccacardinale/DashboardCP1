# dashboard_cp1.py
# -------------------------------------------------------------
# CP1 Dashboard - Streamlit
# Lucca Ribeiro Cardinale RM556668
# -------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(
    page_title="CP1 - Dashboard Profissional + Análise de Dados",
    layout="wide",
)


# Funções auxiliares

@st.cache_data(show_spinner=False)
def carregar_csv(arquivo) -> pd.DataFrame:
    if arquivo is None:
        caminho_padrao = Path("Global_Cybersecurity_Threats_2015-2024.csv")
        if caminho_padrao.exists():
            df = pd.read_csv(caminho_padrao)
        else:
            return pd.DataFrame()
    else:
        if hasattr(arquivo, "read"):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_csv(str(arquivo))


    # Tradução de colunas


    mapa_colunas = {
        "Year": "Ano",
        "Region": "Região",
        "Country": "País",
        "Threat_Type": "Tipo de Ameaça",
        "Severity": "Severidade",
        "Incidents": "Incidentes",
        "Loss_USD": "Perda_USD",
    }
    df = df.rename(columns=mapa_colunas)
    return df

def detectar_tipos(df: pd.DataFrame):
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    colunas_categoricas = df.select_dtypes(exclude=[np.number]).columns.tolist()
    return colunas_numericas, colunas_categoricas

def intervalo_confianca_media(serie: pd.Series, confianca: float = 0.95):
    """Calcula o intervalo de confiança da média usando t-student."""
    x = serie.dropna().values.astype(float)
    n = len(x)
    if n < 2:
        return np.nan, np.nan
    media = np.mean(x)
    erro = stats.sem(x, nan_policy="omit")
    h = stats.t.ppf((1 + confianca) / 2., n - 1) * erro
    return media - h, media + h


# Barra lateral - Navegação

with st.sidebar:
    st.title("Navegação")
    aba = st.radio(
        "Escolha uma aba",
        ["Sobre mim", "Formação", "Competências", "Análise de Dados"],
        index=0
    )
    st.markdown("---")
    st.caption("CP1 • Streamlit • Estatística Aplicada")


# Aba Início

if aba == "Sobre mim":
    st.title("Olá! Meu nome é Lucca Ribeiro Cardinale!")
    st.caption("Tenho 19 anos, sempre fui muito conectado com o mundo digital e o que ele tem a oferecer e sempre na procura de coisas novas para aprender.Este dashboard foi desenvolvido para o **CP1** da disciplina, unindo **apresentação profissional** e uma **análise de dados** aplicada.Use o menu lateral para navegar entre as abas.")
    st.subheader("Objetivo Profissional")
    st.write(
        """
       Atuar como **Profissional de Cybersegurança**, para tornar a internet um lugar mais seguro e conseguir evoluir na área.  
        """
    )
    st.write("Contato: luccarcardinale@gmail.com")
    st.write("GitHub: https://github.com/luccacardinale")
    st.write("LinkedIn: https://www.linkedin.com/in/lucca-cardinale-5064562b6?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")


# Aba Formação

elif aba == "Formação":
    st.title("Formação Acadêmica")
    st.markdown(
        """
        ### Formação
        - **Bacharelado em Engenharia de Software** — FIAP (2024 – 2028)
        - **Cursos relevantes:** Python, React, Estatística Aplicada , SQL , Linux , Cisco Packet Tracer, Java
        ### Certificações
        - Nano Courses - FIAP
        - Cybersecurity - Alura
        """
    )


# Aba Competências

elif aba == "Competências":
    st.title("Competências Técnicas e Comportamentais")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hard Skills")
        st.markdown(
            """
            - Python (Pandas, NumPy, Scipy, Plotly)
            - SQL e Modelagem de Dados
            - Noções de Cibersegurança
            - Noções de Linux
            """
        )
    with col2:
        st.subheader("Soft Skills")
        st.markdown(
            """
            - Flexibilidade
            - Trabalho em Equipe
            - Resolução de Problemas
            - Organização e Proatividade
            """
        )


# Aba Análise de Dados

elif aba == "Análise de Dados":
    st.title("Análise de Dados — Ameaças Cibernéticas 🌐🔒")
    st.caption("O conjunto de dados Global Cybersecurity Threats (2015–2024) reúne informações sobre incidentes de cibersegurança registrados ao longo de dez anos em diferentes regiões e países. Ele contém variáveis como Ano, Região, País, Tipo de Ameaça, Severidade, Número de Incidentes e Perdas Financeiras em USD.Esse dataset permite analisar tanto a evolução temporal dos ataques quanto a distribuição geográfica e por tipo de ameaça, além de possibilitar a investigação de padrões de severidade e impacto financeiro. A partir dele, é possível responder a perguntas como: quais regiões concentram mais incidentes, quais ameaças geram maiores perdas e como a frequência dos ataques tem variado ao longo do tempo.")

    # --- Carregamento de dados
    st.subheader("Carregamento dos Dados")
    arquivo = st.file_uploader("Faça upload do CSV (ou deixe em branco para usar o arquivo padrão)", type=["csv"])
    df = carregar_csv(arquivo)

    if df.empty:
        st.warning(
            "Nenhum dado carregado. Faça upload de um CSV ou coloque "
            "`Global_Cybersecurity_Threats_2015-2024.csv` na mesma pasta do app."
        )
        st.stop()

    colunas_numericas, colunas_categoricas = detectar_tipos(df)

    # 1) Apresentação dos dados
    st.markdown("### 1) Apresentação dos dados e tipos de variáveis")
    with st.expander("Ver amostra e esquema", expanded=True):
        st.write("**Amostra (head):**")
        st.dataframe(df.head(), use_container_width=True)

        st.write("**Tipos de variáveis (dtypes):**")
        st.dataframe(df.dtypes.astype(str), use_container_width=True)

        st.write("**Identificação automática:**")
        st.write(
            f"- **Numéricas:** {', '.join(colunas_numericas) if colunas_numericas else '—'}  \n"
            f"- **Categóricas:** {', '.join(colunas_categoricas) if colunas_categoricas else '—'}"
        )
    st.markdown("**Perguntas de análise:**")
    st.write("- Qual foi o ataque que causou mais prejuizo?")
    st.write("- Quais são os tipos de ameaças mais comuns?")
    st.write("- Qual pais que sofreu mais ataques?")

    # Estatística descritiva
    st.markdown("### 2) Estatística descritiva, distribuições e correlação")
    if colunas_numericas:
        st.write("**Resumo estatístico (variáveis numéricas):**")
        st.dataframe(df[colunas_numericas].describe().T, use_container_width=True)

        # Distribuição
        variavel_num = st.selectbox("Escolha uma variável numérica para visualizar a distribuição:", colunas_numericas, index=0)
        fig_hist = px.histogram(df, x=variavel_num, nbins=30, marginal="box", opacity=0.85)
        st.plotly_chart(fig_hist, use_container_width=True)

        try:
            moda = df[variavel_num].mode().iloc[0]
        except:
            moda = "—"

        media = df[variavel_num].mean()
        mediana = df[variavel_num].median()
        variancia = df[variavel_num].var()
        desvio_padrao = df[variavel_num].std()

        st.write(
            f"**Média:** {media:.2f} | **Mediana:** {mediana:.2f} | "
            f"**Moda:** {moda} | **Variância:** {variancia:.2f} | **Desvio Padrão:** {desvio_padrao:.2f}"
        )

        # Comentário interpretativo resumido
        st.markdown(
            f"""
            A variável **{variavel_num}** apresenta média de **{media:.2f}**, mediana de **{mediana:.2f}** e moda igual a **{moda}**.  
            O desvio padrão de **{desvio_padrao:.2f}** mostra que há {'grande' if desvio_padrao > media else 'baixa'} dispersão em relação à média, 
            indicando a presença de possíveis **outliers**.  
            Nesse contexto, a **mediana** costuma representar melhor o valor típico do que a média.
            """
        )

        # Correlação
        if len(colunas_numericas) >= 2:
            corr = df[colunas_numericas].corr(numeric_only=True)
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Matriz de Correlação (numéricas)")
            st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("Discussão sobre a distribuição dos dados:")
        st.write(" A variável analisada apresenta assimetria à direita, com muitos casos em valores baixos e poucos em níveis muito altos.Isso indica a presença de outliers, que representam ataques raros mas de grande impacto.Nessa situação, a mediana descreve melhor o caso típico do que a média.")



    # Série temporal (corrigida)
    colunas_tempo = [c for c in df.columns if "ano" in c.lower() or "data" in c.lower()]
    if colunas_tempo and colunas_numericas:
        st.markdown("**Tendência temporal (se aplicável):**")
        coluna_tempo = st.selectbox("Selecione a coluna de tempo:", colunas_tempo, index=0)

        # evita escolher a mesma coluna como métrica
        opcoes_metricas = [c for c in colunas_numericas if c != coluna_tempo]
        if not opcoes_metricas:
            st.info("Não há métrica numérica distinta da coluna de tempo para plotar a série temporal.")
        else:
            valor_coluna = st.selectbox("Selecione a métrica numérica:", opcoes_metricas)
            ts = (
                df.groupby(coluna_tempo)[valor_coluna]
                  .mean()
                  .reset_index(name=f"média_{valor_coluna}")
                  .sort_values(coluna_tempo)
            )
            fig_ts = px.line(
                ts, x=coluna_tempo, y=f"média_{valor_coluna}",
                markers=True, title=f"Evolução temporal de {valor_coluna}"
            )
            st.plotly_chart(fig_ts, use_container_width=True)

    # Intervalos de Confiança e Teste de Hipótese
    st.markdown("### 3) Intervalos de Confiança e Testes de Hipótese")
    if not colunas_numericas or not colunas_categoricas:
        st.info("Para IC/Teste de Hipótese, selecione pelo menos **1 variável numérica** e **1 categórica** no seu dataset.")
    else:
        alvo_num = st.selectbox("Variável numérica (alvo)", colunas_numericas, index=0)
        grupo_cat = st.selectbox("Variável categórica (grupos)", colunas_categoricas, index=0)
        confianca = st.slider("Nível de confiança", min_value=80, max_value=99, value=95, step=1)

        # IC por grupo
        grupos = df[[grupo_cat, alvo_num]].dropna().groupby(grupo_cat)
        resultados = []
        for g, sub in grupos:
            inferior, superior = intervalo_confianca_media(sub[alvo_num], confianca/100.0)
            resultados.append({
                grupo_cat: g,
                "n": len(sub),
                "média": float(np.mean(sub[alvo_num])),
                f"IC{confianca}%_inferior": inferior,
                f"IC{confianca}%_superior": superior
            })
        df_ic = pd.DataFrame(resultados).sort_values("média", ascending=False)
        st.dataframe(df_ic, use_container_width=True)

        # Teste t entre 2 grupos
        st.subheader("Teste de Hipótese")
        opcoes = df[grupo_cat].dropna().unique().tolist()
        selecionados = st.multiselect("Selecione 2 grupos para comparar", opcoes, default=opcoes[:2])
        if len(selecionados) == 2:
            g1 = df[df[grupo_cat] == selecionados[0]][alvo_num].dropna()
            g2 = df[df[grupo_cat] == selecionados[1]][alvo_num].dropna()
            if len(g1) > 1 and len(g2) > 1:
                t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
                st.write(f"**H0:** a média de {alvo_num} é igual entre {selecionados[0]} e {selecionados[1]}.")
                st.write(f"**H1:** as médias são diferentes.")
                st.metric("t-statistic", f"{t_stat:.3f}")
                st.metric("p-valor", f"{p_val:.4f}")
