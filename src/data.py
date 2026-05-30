"""Data utilities shared by PlantVillage research notebooks.

The notebooks in this project use the same metadata split, PyTorch Dataset,
subsetting strategy, sampler weights, and resampling helpers. Keeping these
functions here makes each notebook shorter and keeps experimental settings
consistent across phases.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


@dataclass(frozen=True)
class ProjectPaths:
    """Common project paths used by the notebooks."""

    project_dir: Path = Path(__file__).resolve().parents[1]

    @property
    def base_dir(self) -> Path:
        return self.project_dir / "data" / "raw"

    @property
    def metadata_dir(self) -> Path:
        return self.project_dir / "metadata"

    def results_dir(self, phase_name: str) -> Path:
        return self.project_dir / "results" / phase_name

    def reports_dir(self, phase_name: str) -> Path:
        return self.project_dir / "reports" / phase_name


def ensure_directories(*directories: Path) -> None:
    """Create output directories if they do not exist."""

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def create_metadata_splits(
    raw_dir: Path,
    output_dir: Path,
    dataset_name: str = "color",
    test_size: float = 0.20,
    val_size_from_temp: float = 0.50,
    seed: int = 42,
) -> None:
    """Create stratified train/validation/test metadata files.

    The metadata files are saved as CSV so later notebooks can reuse the exact
    same split and avoid accidental train/test drift.
    """

    dataset_dir = raw_dir / dataset_name
    records = []

    for class_dir in sorted(dataset_dir.iterdir()):
        if not class_dir.is_dir():
            continue

        for image_path in sorted(class_dir.iterdir()):
            if image_path.suffix.lower() in IMAGE_EXTENSIONS:
                records.append(
                    {
                        "relative_path": f"{class_dir.name}/{image_path.name}",
                        "class_name": class_dir.name,
                    }
                )

    df = pd.DataFrame(records)
    class_names = sorted(df["class_name"].unique())
    class_to_id = {class_name: idx for idx, class_name in enumerate(class_names)}
    df["class_id"] = df["class_name"].map(class_to_id)

    train_df, temp_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df["class_id"],
        random_state=seed,
    )
    val_df, test_df = train_test_split(
        temp_df,
        test_size=val_size_from_temp,
        stratify=temp_df["class_id"],
        random_state=seed,
    )

    ensure_directories(output_dir)
    train_df.to_csv(output_dir / "train.csv", index=False)
    val_df.to_csv(output_dir / "val.csv", index=False)
    test_df.to_csv(output_dir / "test.csv", index=False)
    pd.DataFrame(
        list(class_to_id.items()),
        columns=["class_name", "class_id"],
    ).to_csv(output_dir / "class_map.csv", index=False)


def load_metadata(metadata_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load train, validation, test, and class map metadata."""

    train_df = pd.read_csv(metadata_dir / "train.csv")
    val_df = pd.read_csv(metadata_dir / "val.csv")
    test_df = pd.read_csv(metadata_dir / "test.csv")
    class_map_df = pd.read_csv(metadata_dir / "class_map.csv")
    return train_df, val_df, test_df, class_map_df


def subset_by_class_head(
    df: pd.DataFrame,
    samples_per_class: int,
    min_samples_per_class: int | None = None,
) -> pd.DataFrame:
    """Fast deterministic subset for debugging or quick baseline runs."""

    if min_samples_per_class is None:
        min_samples_per_class = samples_per_class

    return (
        df.groupby("class_id", group_keys=False)
        .head(max(samples_per_class, min_samples_per_class))
        .reset_index(drop=True)
    )


def create_imbalanced_subset(
    df: pd.DataFrame,
    majority_fraction: float = 0.20,
    minority_fraction: float = 0.45,
    threshold: int = 500,
    min_samples: int = 40,
    seed: int = 42,
) -> pd.DataFrame:
    """Create a controlled subset while preserving the natural imbalance."""

    subset_dfs = []

    for _, group in df.groupby("class_id"):
        class_count = len(group)
        fraction = majority_fraction if class_count >= threshold else minority_fraction
        n_samples = int(class_count * fraction)
        n_samples = max(min_samples, n_samples)
        n_samples = min(n_samples, class_count)
        subset_dfs.append(group.sample(n=n_samples, random_state=seed))

    return pd.concat(subset_dfs).sample(frac=1, random_state=seed).reset_index(drop=True)


def create_stratified_subset(
    df: pd.DataFrame,
    fraction: float = 0.30,
    min_samples: int = 8,
    seed: int = 42,
) -> pd.DataFrame:
    """Create a stratified validation/test subset that keeps every class."""

    subset_dfs = []

    for _, group in df.groupby("class_id"):
        n_samples = max(min_samples, int(len(group) * fraction))
        n_samples = min(n_samples, len(group))
        subset_dfs.append(group.sample(n=n_samples, random_state=seed))

    return pd.concat(subset_dfs).sample(frac=1, random_state=seed).reset_index(drop=True)


def create_hybrid_resampled_dataset(
    df: pd.DataFrame,
    target_size: int,
    seed: int = 42,
) -> pd.DataFrame:
    """Undersample majority classes and oversample minority classes."""

    resampled_dfs = []

    for _, group in df.groupby("class_id"):
        if len(group) >= target_size:
            resampled_group = group.sample(n=target_size, random_state=seed)
        else:
            repeat_factor = (target_size // len(group)) + 1
            repeated_group = pd.concat([group] * repeat_factor).reset_index(drop=True)
            resampled_group = repeated_group.sample(n=target_size, random_state=seed)
        resampled_dfs.append(resampled_group)

    return pd.concat(resampled_dfs).sample(frac=1, random_state=seed).reset_index(drop=True)


class PlantDataset(Dataset):
    """PyTorch dataset for PlantVillage metadata rows."""

    def __init__(
        self,
        df: pd.DataFrame,
        base_dir: Path,
        dataset_name: str = "color",
        transform=None,
    ) -> None:
        self.df = df.reset_index(drop=True)
        self.base_dir = Path(base_dir)
        self.dataset_name = dataset_name
        self.transform = transform

    def __len__(self) -> int:
        return len(self.df)

    def _resolve_image_path(self, row: pd.Series) -> Path:
        relative_path = row["relative_path"]
        image_path = self.base_dir / self.dataset_name / relative_path

        if self.dataset_name == "segmented" and not image_path.exists():
            path = Path(relative_path)
            class_name = row["class_name"]
            image_path = self.base_dir / "segmented" / class_name / f"{path.stem}_final_masked{path.suffix}"

        if not image_path.exists():
            image_path = self.base_dir / "color" / relative_path

        return image_path

    def __getitem__(self, idx: int):
        row = self.df.iloc[idx]
        image = Image.open(self._resolve_image_path(row)).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, int(row["class_id"])


def get_class_counts(df: pd.DataFrame) -> pd.Series:
    """Return class counts sorted by class id."""

    return df["class_id"].value_counts().sort_index()


def get_num_classes(class_map_df: pd.DataFrame | None = None, df: pd.DataFrame | None = None) -> int:
    """Infer number of classes from class map or dataframe."""

    if class_map_df is not None:
        return int(class_map_df["class_id"].nunique())
    if df is not None:
        return int(df["class_id"].nunique())
    raise ValueError("Provide class_map_df or df to infer number of classes.")


def compute_inverse_frequency_weights(
    class_counts: pd.Series,
    num_classes: int | None = None,
    normalize_to_num_classes: bool = True,
) -> np.ndarray:
    """Compute inverse-frequency class weights."""

    if num_classes is None:
        num_classes = int(class_counts.index.max()) + 1

    counts = np.ones(num_classes, dtype=np.float32)
    for class_id, count in class_counts.items():
        counts[int(class_id)] = max(float(count), 1.0)

    weights = 1.0 / counts
    if normalize_to_num_classes:
        weights = weights / weights.sum() * num_classes

    return weights.astype(np.float32)


def compute_sample_weights(df: pd.DataFrame, class_weights: np.ndarray) -> list[float]:
    """Map each dataframe row to its class weight."""

    return [float(class_weights[int(class_id)]) for class_id in df["class_id"]]


def build_data_loader(
    df: pd.DataFrame,
    base_dir: Path,
    dataset_name: str,
    transform,
    batch_size: int,
    shuffle: bool = False,
    sampler=None,
    num_workers: int = 0,
    pin_memory: bool = False,
) -> DataLoader:
    """Build a DataLoader from metadata rows."""

    dataset = PlantDataset(
        df=df,
        base_dir=base_dir,
        dataset_name=dataset_name,
        transform=transform,
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle if sampler is None else False,
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )


def build_weighted_sampler(
    df: pd.DataFrame,
    class_weights: np.ndarray,
    replacement: bool = True,
) -> WeightedRandomSampler:
    """Create a WeightedRandomSampler using class-level weights."""

    sample_weights = compute_sample_weights(df, class_weights)
    return WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=replacement,
    )
