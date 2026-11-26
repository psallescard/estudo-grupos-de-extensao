import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_empilhado(df_in, pares_xy, titulo_legenda="", cmap="Blues", figsize=(13, 4)):
    """Plota barras 100% empilhadas verticais para uma lista de (col_x, col_y, titulo)."""
    fig, axes = plt.subplots(1, len(pares_xy), figsize=figsize, squeeze=False)
    for ax, (cx, cy, titulo) in zip(axes[0], pares_xy):
        ct = pd.crosstab(df_in[cx], df_in[cy], normalize="index") * 100
        counts = df_in[cx].value_counts().reindex(ct.index)
        ct.index = [f"{idx}\n(n={n})" for idx, n in zip(ct.index, counts)]

        ct.plot(
            kind="bar", stacked=True, colormap=cmap, ax=ax, width=0.55, edgecolor="white", legend=(ax == axes[0][-1])
        )
        ax.set(title=titulo, xlabel="", ylabel="% dos Alunos" if ax == axes[0][0] else "", ylim=(0, 100))
        ax.tick_params(axis="x", rotation=15)

    axes[0][-1].legend(title=titulo_legenda, bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
    plt.tight_layout()
    plt.show()


def plot_ic_media(df_in, pares_xy, ylabel="Média Esperada (IC 95%)", figsize=(13, 4), sharey=True):
    """Plota point plots com IC 95% da média para uma lista de (col_x, col_y_num, titulo)."""
    fig, axes = plt.subplots(1, len(pares_xy), figsize=figsize, sharey=sharey, squeeze=False)
    for ax, (cx, cy, titulo) in zip(axes[0], pares_xy):
        sns.pointplot(data=df_in, x=cx, y=cy, errorbar=("ci", 95), capsize=0.15, color="#1e3a8a", ax=ax)
        ax.set(title=titulo, xlabel="", ylabel=ylabel if ax == axes[0][0] else "")
        ax.tick_params(axis="x", rotation=15)

    plt.tight_layout()
    plt.show()
