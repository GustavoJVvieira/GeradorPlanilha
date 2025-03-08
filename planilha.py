import pandas as pd

# Caminho dos arquivos CSV
arquivo_videos = "relatorio_videos.csv"
arquivo_exercicios = "relatorio_exercicios.csv"
arquivo_saida = "tempo_total_por_aluno.csv"

# Função para converter tempo hh:mm:ss para segundos
def tempo_para_segundos(tempo_str):
    try:
        if pd.isna(tempo_str) or tempo_str.strip() == "":
            return 0  # Se estiver vazio ou NaN, retorna 0
        partes = tempo_str.split(":")
        if len(partes) == 2:  # Caso esteja no formato MM:SS
            partes = ["00"] + partes  # Adiciona horas como 00
        h, m, s = map(int, partes)
        return h * 3600 + m * 60 + s
    except Exception as e:
        print(f"Erro ao processar tempo {tempo_str}: {e}")
        return 0

# Função para converter segundos para HH:MM:SS
def segundos_para_hms(segundos):
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return f"{int(h):02}:{int(m):02}:{int(s):02}"

# Carregar CSVs
df_videos = pd.read_csv(arquivo_videos, sep=";", engine="python")
df_exercicios = pd.read_csv(arquivo_exercicios, sep=";", engine="python")

# Padronizar e-mails (remover espaços extras e colocar tudo em minúsculas)
df_videos["Email"] = df_videos["Email"].str.strip().str.lower()
df_exercicios["Email"] = df_exercicios["Email"].str.strip().str.lower()

# Converter tempo para segundos
df_videos["Tempo Assistido Total"] = df_videos["Tempo Assistido Total"].apply(tempo_para_segundos)
df_exercicios["Tempo Estimado"] = df_exercicios["Tempo Estimado"].apply(tempo_para_segundos)

# Somar os tempos corretamente agrupando por e-mail
df_videos_agrupado = df_videos.groupby("Email", as_index=False)["Tempo Assistido Total"].sum()
df_exercicios_agrupado = df_exercicios.groupby("Email", as_index=False)["Tempo Estimado"].sum()

# Renomear colunas
df_videos_agrupado.rename(columns={"Tempo Assistido Total": "Tempo Total Vídeos"}, inplace=True)
df_exercicios_agrupado.rename(columns={"Tempo Estimado": "Tempo Total Exercícios"}, inplace=True)

# Mesclar os dois DataFrames
df_final = pd.merge(df_videos_agrupado, df_exercicios_agrupado, on="Email", how="outer").fillna(0)

# Criar coluna de tempo total somado
df_final["Tempo Total"] = df_final["Tempo Total Vídeos"] + df_final["Tempo Total Exercícios"]

# Converter tudo de volta para HH:MM:SS
df_final["Tempo Total Vídeos"] = df_final["Tempo Total Vídeos"].apply(segundos_para_hms)
df_final["Tempo Total Exercícios"] = df_final["Tempo Total Exercícios"].apply(segundos_para_hms)
df_final["Tempo Total"] = df_final["Tempo Total"].apply(segundos_para_hms)

# Salvar CSV final
df_final.to_csv(arquivo_saida, sep=";", index=False)

print(f"Arquivo final criado com sucesso: {arquivo_saida}")
