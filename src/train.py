"""Training, evaluation, and loss helpers for PyTorch experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class TrainConfig:
    """Shared training configuration for notebook experiments."""

    epochs: int = 15
    batch_size: int = 64
    learning_rate: float = 1e-3
    patience: int = 3
    monitor: str = "val_macro_f1"
    use_early_stopping: bool = True


class FocalLoss(nn.Module):
    """Multi-class focal loss for class imbalance research."""

    def __init__(self, gamma: float = 2.0, weight: torch.Tensor | None = None, reduction: str = "mean"):
        super().__init__()
        self.gamma = gamma
        self.weight = weight
        self.reduction = reduction

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(logits, targets, weight=self.weight, reduction="none")
        pt = torch.exp(-ce_loss)
        focal_loss = (1 - pt) ** self.gamma * ce_loss

        if self.reduction == "mean":
            return focal_loss.mean()
        if self.reduction == "sum":
            return focal_loss.sum()
        return focal_loss


def effective_number_class_weights(
    class_counts: pd.Series,
    num_classes: int,
    beta: float = 0.999,
    normalize_to_num_classes: bool = True,
) -> np.ndarray:
    """Compute Class-Balanced Loss weights from effective number of samples."""

    counts = np.ones(num_classes, dtype=np.float32)
    for class_id, count in class_counts.items():
        counts[int(class_id)] = max(float(count), 1.0)

    effective_num = 1.0 - np.power(beta, counts)
    weights = (1.0 - beta) / np.maximum(effective_num, 1e-8)

    if normalize_to_num_classes:
        weights = weights / weights.sum() * num_classes

    return weights.astype(np.float32)


def train_model(
    model: nn.Module,
    train_loader,
    val_loader,
    criterion,
    optimizer,
    epochs: int,
    device,
    save_path: Path,
    patience: int = 3,
    use_early_stopping: bool = True,
) -> dict[str, list[float]]:
    """Train a model and save the best checkpoint by Validation Macro F1."""

    model = model.to(device)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    best_val_f1 = -1.0
    patience_counter = 0
    history = {"train_loss": [], "val_loss": [], "val_f1": [], "val_acc": []}

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0

        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * inputs.size(0)

        train_loss /= len(train_loader.dataset)

        val_loss, val_acc, val_macro_f1 = evaluate_validation_loss(
            model=model,
            val_loader=val_loader,
            criterion=criterion,
            device=device,
        )

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_f1"].append(val_macro_f1)
        history["val_acc"].append(val_acc)

        print(
            f"Epoch {epoch:02d}/{epochs:02d} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Val Loss: {val_loss:.4f} | "
            f"Val Acc: {val_acc:.4f} | "
            f"Val Macro F1: {val_macro_f1:.4f}"
        )

        if val_macro_f1 > best_val_f1:
            best_val_f1 = val_macro_f1
            torch.save(model.state_dict(), save_path)
            patience_counter = 0
        else:
            patience_counter += 1
            if use_early_stopping and patience_counter >= patience:
                print(
                    f"-> EarlyStopping tại epoch {epoch}: "
                    f"Validation Macro F1 không cải thiện sau {patience} epoch."
                )
                break

    return history


def evaluate_validation_loss(model: nn.Module, val_loader, criterion, device) -> tuple[float, float, float]:
    """Evaluate validation loss, accuracy, and Macro F1."""

    model.eval()
    val_loss = 0.0
    preds = []
    labels = []

    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs = inputs.to(device)
            targets = targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            val_loss += loss.item() * inputs.size(0)
            preds.extend(outputs.argmax(dim=1).cpu().numpy())
            labels.extend(targets.cpu().numpy())

    val_loss /= len(val_loader.dataset)
    val_acc = accuracy_score(labels, preds)
    _, _, val_macro_f1, _ = precision_recall_fscore_support(
        labels,
        preds,
        average="macro",
        zero_division=0,
    )
    return val_loss, val_acc, val_macro_f1


def evaluate_model(model: nn.Module, test_loader, device, num_classes: int) -> dict:
    """Evaluate model with global and per-class classification metrics."""

    model.eval()
    preds = []
    labels = []

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            preds.extend(outputs.argmax(dim=1).cpu().numpy())
            labels.extend(targets.numpy())

    class_labels = list(range(num_classes))
    acc = accuracy_score(labels, preds)
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        labels,
        preds,
        average="macro",
        zero_division=0,
    )
    per_precision, per_recall, per_f1, _ = precision_recall_fscore_support(
        labels,
        preds,
        labels=class_labels,
        zero_division=0,
    )
    cm = confusion_matrix(labels, preds, labels=class_labels)
    
    return {
        "accuracy": acc,
        "macro_f1": macro_f1,
        "precision": macro_precision,
        "recall": macro_recall,
        "per_class_precision": per_precision,
        "per_class_recall": per_recall,
        "per_class_f1": per_f1,
        "confusion_matrix": cm,
        "preds": preds,
        "labels": labels,
    }

