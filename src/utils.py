"""General utilities for reproducible experiments and reporting."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torchvision.transforms as transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def set_seed(seed: int = 42) -> None:
    """Set random seeds for reproducible experiments."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    """Return the best available device for the local machine."""

    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def get_pin_memory(device: torch.device) -> bool:
    """Use pin_memory only when CUDA is available."""

    return device.type == "cuda"


def get_num_workers(device: torch.device, notebook_safe: bool = True) -> int:
    """Return a safe DataLoader worker count.

    On macOS/MPS notebooks, multiprocessing frequently fails because notebook
    classes are not pickleable. The default therefore stays at 0.
    """

    if notebook_safe:
        return 0
    return 2 if device.type == "cuda" else 0


def get_basic_transform(image_size: int):
    """Resize, convert to tensor, and normalize using ImageNet statistics."""

    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )


def get_light_augmentation_transform(image_size: int):
    """Light augmentation suitable for plant disease images."""

    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )


def get_augmentation_transforms(image_size: int) -> dict:
    """Standard augmentation search space for Phase 04."""

    baseline = get_basic_transform(image_size)
    return {
        "baseline": baseline,
        "exp1_flip": transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.ToTensor(),
                transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
            ]
        ),
        "exp2_rotation": transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.RandomRotation(degrees=15),
                transforms.ToTensor(),
                transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
            ]
        ),
        "exp3_flip_rot": transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(degrees=15),
                transforms.ToTensor(),
                transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
            ]
        ),
        "exp4_jitter": transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
                transforms.ToTensor(),
                transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
            ]
        ),
        "exp5_erasing": transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.ToTensor(),
                transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
                transforms.RandomErasing(p=0.5, scale=(0.02, 0.2), ratio=(0.3, 3.3)),
            ]
        ),
    }


def dataframe_to_markdown_safe(dataframe: pd.DataFrame, index: bool = False) -> str:
    """Convert a DataFrame to markdown with a robust fallback."""

    try:
        return dataframe.to_markdown(index=index)
    except Exception:
        return dataframe.to_string(index=index)


def write_text_report(path: Path, sections: list[str]) -> None:
    """Write a text or markdown report from prebuilt sections."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(sections), encoding="utf-8")

