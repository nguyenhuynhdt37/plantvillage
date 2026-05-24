"""Reusable plotting utilities for research notebooks."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix


def set_publication_style() -> None:
    """Apply a clean plotting style for report-ready figures."""

    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 110,
            "savefig.dpi": 300,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 9,
        }
    )


def annotate_bars(ax, fmt: str = "{:.2f}", y_offset: float = 0.01) -> None:
    """Annotate bar values above each bar."""

    for patch in ax.patches:
        height = patch.get_height()
        ax.text(
            patch.get_x() + patch.get_width() / 2,
            height + y_offset,
            fmt.format(height),
            ha="center",
            va="bottom",
            fontsize=9,
        )


def save_figure(path: Path) -> None:
    """Save current matplotlib figure with consistent quality."""

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")


def plot_metric_bars(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    hue: str | None = None,
    title: str | None = None,
    save_path: Path | None = None,
    rotate_xticks: int = 20,
    ylim: tuple[float, float] = (0, 1.05),
) -> None:
    """Plot a compact metric comparison bar chart."""

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=dataframe, x=x, y=y, hue=hue, ax=ax)
    ax.set_title(title or f"{y} comparison", fontweight="bold")
    ax.set_ylim(*ylim)
    ax.tick_params(axis="x", rotation=rotate_xticks)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    annotate_bars(ax)

    if save_path:
        save_figure(save_path)
    plt.show()


def plot_learning_curves(
    histories: dict[str, dict[str, list[float]]],
    save_path: Path | None = None,
    title: str = "Learning Curves",
) -> None:
    """Plot train loss, validation loss, and validation Macro F1."""

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for experiment_name, history in histories.items():
        epochs_range = range(1, len(history["train_loss"]) + 1)
        axes[0].plot(epochs_range, history["train_loss"], marker="o", label=experiment_name)
        axes[1].plot(epochs_range, history["val_loss"], marker="o", label=experiment_name)
        axes[2].plot(epochs_range, history["val_f1"], marker="o", label=experiment_name)

    axes[0].set_title("Train Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")

    axes[1].set_title("Validation Loss")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")

    axes[2].set_title("Validation Macro F1")
    axes[2].set_xlabel("Epoch")
    axes[2].set_ylabel("Macro F1")
    axes[2].set_ylim(0, 1)

    for ax in axes:
        ax.grid(True, linestyle="--", alpha=0.4)

    axes[2].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    fig.suptitle(title, fontsize=15, fontweight="bold")

    if save_path:
        save_figure(save_path)
    plt.show()


def plot_confusion_heatmap(
    y_true,
    y_pred,
    labels: list[int],
    class_names: list[str] | None = None,
    normalize: str | None = None,
    title: str = "Confusion Matrix",
    save_path: Path | None = None,
    figsize: tuple[int, int] = (16, 13),
) -> np.ndarray:
    """Plot a confusion matrix heatmap and return the matrix."""

    cm = confusion_matrix(y_true, y_pred, labels=labels, normalize=normalize)
    tick_labels = class_names if class_names is not None else labels

    plt.figure(figsize=figsize)
    sns.heatmap(
        cm,
        cmap="Blues",
        xticklabels=tick_labels,
        yticklabels=tick_labels,
        annot=False,
        cbar=True,
    )
    plt.title(title, fontweight="bold")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    if save_path:
        save_figure(save_path)
    plt.show()
    return cm

