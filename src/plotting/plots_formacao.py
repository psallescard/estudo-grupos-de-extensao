"""Figures for front 1 (Formação: extensão vs. Poli). Titles and labels in PT-BR, as required by the README."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

COLOR_EXT = "#0F4C81"  # extension
COLOR_DISC = "#C84B31"  # mandatory courses
COLOR_NEUTRAL = "#6B7280"
CATEGORY_COLORS = {"Consultoria & Negócios": "#0F4C81", "Engenharia": "#C84B31", "Mercado Financeiro": "#2E8B57"}


def _save(fig, path):
    fig.tight_layout()
    if path is not None:
        fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.show()


def _mean_ci(values):
    v = np.asarray(values, dtype=float)
    half = stats.t.ppf(0.975, v.size - 1) * v.std(ddof=1) / np.sqrt(v.size)
    return v.mean(), half


def plot_preparo_distribution(df, path=None):
    """Left: distribution of both 1-5 scales. Right: distribution of the paired difference."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.3), gridspec_kw={"width_ratios": [1.25, 1]})
    levels = [1, 2, 3, 4, 5]
    disc = df["preparo_disciplinas"].value_counts(normalize=True).reindex(levels, fill_value=0) * 100
    ext = df["preparo_extensao"].value_counts(normalize=True).reindex(levels, fill_value=0) * 100
    x = np.arange(len(levels))
    b1 = ax1.bar(x - 0.19, disc, 0.38, color=COLOR_DISC, label="Disciplinas obrigatórias")
    b2 = ax1.bar(x + 0.19, ext, 0.38, color=COLOR_EXT, label="Grupo de extensão")
    ax1.bar_label(b1, fmt="%.0f%%", fontsize=8, padding=2)
    ax1.bar_label(b2, fmt="%.0f%%", fontsize=8, padding=2)
    ax1.set(xticks=x, xticklabels=levels, xlabel="Nota de preparo profissional (1 a 5)", ylabel="% dos respondentes",
            title="(a) Notas atribuídas a cada fonte de preparo")
    ax1.margins(y=0.15)
    ax1.legend(frameon=False)

    d = (df["preparo_extensao"] - df["preparo_disciplinas"]).value_counts().sort_index()
    colors = [COLOR_DISC if v < 0 else (COLOR_NEUTRAL if v == 0 else COLOR_EXT) for v in d.index]
    bars = ax2.bar(d.index.astype(str), d.values, color=colors)
    ax2.bar_label(bars, fontsize=9, padding=2)
    ax2.set(xlabel="Diferença d = extensão − disciplinas", ylabel="Número de alunos",
            title="(b) Diferença por aluno (n = %d)" % len(df))
    ax2.margins(y=0.15)
    for ax in (ax1, ax2):
        sns.despine(ax=ax)
    _save(fig, path)


def _dot_panel(ax, df, group, order, title):
    y = np.arange(len(order))
    for col, color, label, offset in [("preparo_disciplinas", COLOR_DISC, "Disciplinas", 0.13),
                                      ("preparo_extensao", COLOR_EXT, "Extensão", -0.13)]:
        stats_ = [_mean_ci(df.loc[df[group] == level, col]) for level in order]
        ax.errorbar([m for m, _ in stats_], y + offset, xerr=[h for _, h in stats_], fmt="o", color=color,
                    capsize=3, label=label)
    counts = df[group].value_counts()
    ax.set_yticks(y)
    ax.set_yticklabels([f"{level} (n={counts[level]})" for level in order])
    ax.invert_yaxis()
    ax.set(xlim=(1, 5), xlabel="Média (IC 95%)", title=title)
    sns.despine(ax=ax)


def plot_preparo_by_category_and_area(df, category_order, area_order, path=None):
    """Mean of both preparation scores by group category (left) and by course area (right)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.2))
    _dot_panel(ax1, df, "categoria_grupo", category_order, "(a) Por categoria do grupo de extensão")
    _dot_panel(ax2, df, "grande_area_curso", area_order, "(b) Por grande área do curso")
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.06))
    _save(fig, path)


def plot_top_score_share(df, panels, path=None):
    """Share of students giving the top score (5) to the extension, by level of each variable in `panels`
    (list of (column, order, title))."""
    fig, axes = plt.subplots(1, len(panels), figsize=(6.5 * len(panels), 4.2), sharey=True)
    for ax, (col, order, title) in zip(np.atleast_1d(axes), panels):
        share = df.groupby(col, observed=True)["preparo_ext_maximo"].apply(lambda s: (s == "Nota 5").mean() * 100).reindex(order)
        counts = df[col].value_counts().reindex(order)
        bars = ax.bar(range(len(order)), share.values, color=COLOR_EXT)
        ax.bar_label(bars, labels=[f"{v:.0f}%\n(n={n})" for v, n in zip(share.values, counts.values)], fontsize=8, padding=2)
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels(order, rotation=15)
        ax.set(ylim=(0, 115), title=title, ylabel="% que deram nota 5 à extensão")
        sns.despine(ax=ax)
    _save(fig, path)


def plot_goal_means(means_table, order, path=None, xlabel="Importância da média ponderada (média e IC 95%)"):
    """Dot plot of means with t confidence intervals (table from stats_tests.group_means)."""
    table = means_table.reindex(order)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    y = np.arange(len(table))
    ax.errorbar(table["Média"], y, xerr=[table["Média"] - table["IC 95% inf"], table["IC 95% sup"] - table["Média"]],
                fmt="o", color=COLOR_EXT, capsize=4)
    for yi, m in enumerate(table["Média"]):
        ax.annotate(f"{m:.2f}", (m, yi), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{i} (n={int(n)})" for i, n in zip(table.index, table["n"])])
    ax.invert_yaxis()
    ax.set(xlim=(1, 5), xlabel=xlabel, title="Importância atribuída à média por objetivo atual na faculdade")
    sns.despine(ax=ax)
    _save(fig, path)


def plot_regression_scenarios(model, df, category_order, path=None):
    """Predicted net gain as a function of weekly hours, one line per group category, with the 95% confidence
    band of the mean; points are the observed means of each (category, hours band) cell."""
    fig, ax = plt.subplots(figsize=(9, 4.6))
    hours_grid = np.linspace(df["horas_semanais_grupo_num"].min(), df["horas_semanais_grupo_num"].max(), 200)
    for category in category_order:
        grid = pd.DataFrame({"categoria_grupo": pd.Categorical([category] * len(hours_grid), categories=category_order),
                             "log_horas_semanais": np.log(hours_grid)})
        pred = model.get_prediction(grid).summary_frame(alpha=0.05)
        color = CATEGORY_COLORS.get(category, COLOR_NEUTRAL)
        ax.plot(hours_grid, pred["mean"], color=color, label=category)
        ax.fill_between(hours_grid, pred["mean_ci_lower"], pred["mean_ci_upper"], color=color, alpha=0.15)
        observed = df[df["categoria_grupo"] == category].groupby("horas_semanais_grupo_num")["delta_preparo"].agg(["mean", "size"])
        observed = observed[observed["size"] >= 3]
        ax.scatter(observed.index, observed["mean"], color=color, s=observed["size"] * 4, alpha=0.7, edgecolor="white")
    ax.set_xscale("log")
    ticks = sorted(df["horas_semanais_grupo_num"].unique())
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:.0f} h" for t in ticks])
    ax.minorticks_off()
    ax.set(xlabel="Horas semanais no grupo (valor representativo da faixa, escala log)",
           ylabel="Ganho líquido estimado (pontos)",
           title="Ganho líquido estimado pelo modelo final\n(faixa = IC 95% da média; pontos = médias observadas, tamanho "
                 "proporcional a n;\ncombinações com menos de 3 alunos não aparecem)")
    ax.legend(frameon=False, title="Categoria do grupo")
    sns.despine(ax=ax)
    _save(fig, path)


def plot_residual_diagnostics(model, path=None):
    """Residuals vs. fitted values (constant variance, linearity) and normal Q-Q plot (normality)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    # small horizontal jitter: there are only 15 distinct fitted values, so points would pile up in columns
    jitter = np.random.default_rng(0).normal(0, 0.03, len(model.fittedvalues))
    ax1.scatter(model.fittedvalues + jitter, model.resid, alpha=0.5, color=COLOR_EXT, s=15)
    ax1.axhline(0, color="black", lw=0.8, ls="--")
    ax1.set(xlabel="Valor ajustado (com leve deslocamento horizontal para separar os pontos)", ylabel="Resíduo",
            title="(a) Resíduos vs. valores ajustados")
    stats.probplot(model.resid, dist="norm", plot=ax2)
    ax2.get_lines()[0].set(color=COLOR_EXT, markersize=3)
    ax2.get_lines()[1].set(color="black")
    ax2.set(title="(b) Gráfico Q-Q normal dos resíduos", xlabel="Quantis teóricos (normal)", ylabel="Quantis dos resíduos")
    for ax in (ax1, ax2):
        sns.despine(ax=ax)
    _save(fig, path)
