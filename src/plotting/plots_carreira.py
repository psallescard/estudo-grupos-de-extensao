"""Figures for front 3 (Carreira: trajetória & objetivos). Titles and labels in PT-BR, as required by the README."""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.plotting.plots_formacao import COLOR_EXT, COLOR_NEUTRAL, _save, plot_residual_diagnostics

__all__ = ["plot_category_distribution", "plot_stacked_shares", "plot_means_panels", "plot_scenario_probabilities",
           "plot_residual_diagnostics"]


def plot_category_distribution(df, panels, path=None):
    """Horizontal bars with the % of valid answers in each level; `panels` is a list of (categorical column, title)."""
    fig, axes = plt.subplots(1, len(panels), figsize=(5.6 * len(panels), 4.4))
    for ax, (col, title) in zip(np.atleast_1d(axes), panels):
        order = list(df[col].cat.categories)
        counts = df[col].value_counts().reindex(order, fill_value=0)
        share = counts / counts.sum() * 100
        y = np.arange(len(order))
        bars = ax.barh(y, share.values, color=COLOR_EXT)
        ax.bar_label(bars, labels=[f"{v:.0f}% (n={n})" for v, n in zip(share.values, counts.values)], fontsize=8,
                     padding=2)
        ax.set_yticks(y)
        ax.set_yticklabels(order)
        ax.invert_yaxis()
        ax.set(xlim=(0, share.max() * 1.4), xlabel="% das respostas válidas", title=title)
        sns.despine(ax=ax)
    _save(fig, path)


def plot_stacked_shares(observed, title, legend_title, path=None):
    """100% stacked horizontal bars of a contingency table (rows = groups, columns = answers); n of each row in its
    label. Segments below 7% are left without a number to keep the bars readable."""
    shares = observed.div(observed.sum(axis=1), axis=0) * 100
    colors = sns.color_palette("tab10", n_colors=shares.shape[1])
    fig, ax = plt.subplots(figsize=(10, 0.6 * len(shares) + 1.8))
    y = np.arange(len(shares))
    left = np.zeros(len(shares))
    for color, col in zip(colors, shares.columns):
        values = shares[col].to_numpy()
        bars = ax.barh(y, values, left=left, color=color, label=str(col))
        ax.bar_label(bars, labels=[f"{v:.0f}%" if v >= 7 else "" for v in values], label_type="center", fontsize=8,
                     color="white")
        left += values
    ax.set_yticks(y)
    ax.set_yticklabels([f"{level} (n={n})" for level, n in zip(shares.index, observed.sum(axis=1))])
    ax.invert_yaxis()
    ax.set(xlim=(0, 100), xlabel="% dentro de cada linha", title=title)
    ax.legend(title=legend_title, frameon=False, bbox_to_anchor=(1.01, 1), loc="upper left")
    sns.despine(ax=ax)
    _save(fig, path)


def plot_means_panels(panels, path=None):
    """Dot plots of group means with t confidence intervals, one panel per (means table, order, title, xlabel, xlim).
    The tables come from stats_tests.group_means."""
    fig, axes = plt.subplots(1, len(panels), figsize=(6.8 * len(panels), 4.2))
    for ax, (table, order, title, xlabel, xlim) in zip(np.atleast_1d(axes), panels):
        t = table.reindex(order)
        y = np.arange(len(t))
        ax.errorbar(t["Média"], y, xerr=[t["Média"] - t["IC 95% inf"], t["IC 95% sup"] - t["Média"]], fmt="o",
                    color=COLOR_EXT, capsize=4)
        for yi, m in enumerate(t["Média"]):
            ax.annotate(f"{m:.2f}", (m, yi), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
        ax.set_yticks(y)
        ax.set_yticklabels([f"{level} (n={int(n)})" for level, n in zip(t.index, t["n"])])
        ax.invert_yaxis()
        ax.set(xlim=xlim, xlabel=xlabel, title=title)
        sns.despine(ax=ax)
    _save(fig, path)


def plot_scenario_probabilities(model, scenarios, path=None):
    """Estimated probability (%) of planning the first internship up to the 3rd year for each a-priori profile, with
    the 95% confidence interval of the mean. Values outside 0-100% are a known limitation of the linear model."""
    pred = model.get_prediction(scenarios).summary_frame(alpha=0.05) * 100
    y = np.arange(len(scenarios))
    fig, ax = plt.subplots(figsize=(9, 0.35 * len(scenarios) + 1.8))
    ax.errorbar(pred["mean"], y, xerr=[pred["mean"] - pred["mean_ci_lower"], pred["mean_ci_upper"] - pred["mean"]],
                fmt="o", color=COLOR_EXT, capsize=3)
    for limit in (0, 100):
        ax.axvline(limit, color=COLOR_NEUTRAL, lw=0.8, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(scenarios["Cenário"])
    ax.invert_yaxis()
    ax.set(xlabel="Probabilidade estimada de pretender o 1º estágio até o 3º ano (%; IC 95% da média)",
           title="Perfis definidos a priori: intenção de antecipar o estágio (modelo final)")
    sns.despine(ax=ax)
    _save(fig, path)
