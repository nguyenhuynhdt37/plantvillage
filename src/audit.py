"""Dataset audit utilities for PlantVillage EDA notebooks."""

from __future__ import annotations

import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageChops


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def scan_dataset(path: Path) -> pd.DataFrame:
    """Scan one PlantVillage image directory into a dataframe."""

    records = []
    if not path.exists():
        return pd.DataFrame(columns=["class", "path", "filename"])

    for class_dir in sorted(path.iterdir()):
        if not class_dir.is_dir():
            continue
        for image_path in sorted(class_dir.iterdir()):
            if image_path.suffix.lower() in IMAGE_EXTENSIONS:
                records.append(
                    {
                        "class": class_dir.name,
                        "path": image_path,
                        "filename": image_path.name,
                    }
                )

    return pd.DataFrame(records)


def scan_multiple_datasets(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    """Scan multiple dataset variants such as color, grayscale, segmented."""

    return {name: scan_dataset(path) for name, path in paths.items()}


def detect_image_mode(image: Image.Image) -> str:
    """Detect RGB, grayscale, or RGB files that are visually grayscale."""

    mode = image.mode
    if mode == "RGB":
        r, g, b = image.split()
        is_gray_rgb = (
            ImageChops.difference(r, g).getbbox() is None
            and ImageChops.difference(r, b).getbbox() is None
        )
        if is_gray_rgb:
            return "Grayscale (RGB Saved)"
    return mode


def analyze_images(dfs: dict[str, pd.DataFrame], sample_size: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Analyze image size, aspect ratio, and color mode on sampled images."""

    records = []
    for dataset_name, df in dfs.items():
        sample_df = df.sample(min(len(df), sample_size), random_state=seed)
        for path in sample_df["path"]:
            try:
                with Image.open(path) as image:
                    width, height = image.size
                    records.append(
                        {
                            "dataset": dataset_name,
                            "width": width,
                            "height": height,
                            "aspect_ratio": width / height,
                            "mode": detect_image_mode(image),
                        }
                    )
            except Exception:
                continue

    return pd.DataFrame(records)


def compute_dhash(image_path: Path, hash_size: int = 8) -> str:
    """Compute a compact dHash value for duplicate detection."""

    try:
        with Image.open(image_path) as image:
            image = image.resize((hash_size + 1, hash_size), Image.Resampling.BILINEAR).convert("L")
            pixels = np.array(image)
            diff = pixels[:, 1:] > pixels[:, :-1]
            return np.packbits(diff).tobytes().hex()
    except Exception:
        return ""


def find_duplicates_full(df: pd.DataFrame) -> tuple[list, list, dict]:
    """Find intra-class and cross-class duplicate pairs using dHash."""

    paths = df["path"].tolist()
    classes = df["class"].tolist()
    max_workers = min(32, (os.cpu_count() or 1) * 4)
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        hashes = list(executor.map(compute_dhash, paths))

    print(f"Đã băm {len(paths)} ảnh trong {time.time() - start_time:.2f} giây.")

    hash_groups = defaultdict(list)
    for path, class_name, hash_value in zip(paths, classes, hashes):
        if hash_value:
            hash_groups[hash_value].append((path, class_name))

    intra_duplicates = []
    cross_duplicates = []

    for hash_value, items in hash_groups.items():
        if len(items) <= 1:
            continue
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                path_1, class_1 = items[i]
                path_2, class_2 = items[j]
                if class_1 == class_2:
                    intra_duplicates.append((path_1, path_2, hash_value))
                else:
                    cross_duplicates.append((path_1, path_2, hash_value))

    return intra_duplicates, cross_duplicates, hash_groups


def compute_imbalance_metrics(df: pd.DataFrame, class_column: str = "class") -> tuple[float, float, float]:
    """Compute Shannon entropy, normalized entropy, and Gini coefficient."""

    counts = df[class_column].value_counts()
    probabilities = counts / counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    num_classes = len(counts)
    max_entropy = np.log2(num_classes)
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 1.0

    sorted_counts = np.sort(counts.values)
    k = len(sorted_counts)
    gini = (2 * np.sum(np.arange(1, k + 1) * sorted_counts)) / (k * np.sum(sorted_counts)) - (k + 1) / k
    return float(entropy), float(normalized_entropy), float(gini)


def summarize_dataset_by_class(dfs: dict[str, pd.DataFrame], sample_per_class: int = 5, seed: int = 42) -> pd.DataFrame:
    """Build a compact per-class image summary table for dataset audit."""

    records = []
    for dataset_name, df in dfs.items():
        for class_name, group in df.groupby("class"):
            sampled = group["path"].sample(min(len(group), sample_per_class), random_state=seed)
            widths, heights, modes = [], [], []

            for path in sampled:
                try:
                    with Image.open(path) as image:
                        widths.append(image.size[0])
                        heights.append(image.size[1])
                        modes.append(detect_image_mode(image))
                except Exception:
                    continue

            records.append(
                {
                    "dataset_name": dataset_name,
                    "class_name": class_name,
                    "image_count": len(group),
                    "image_mode": max(set(modes), key=modes.count) if modes else "RGB",
                    "avg_width": np.mean(widths) if widths else 256.0,
                    "avg_height": np.mean(heights) if heights else 256.0,
                }
            )

    return pd.DataFrame(records)

