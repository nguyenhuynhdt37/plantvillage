"""PyTorch model definitions shared across PlantVillage notebooks."""

from __future__ import annotations

import torch
import torch.nn as nn
import torchvision.models as models


class SimpleCNN(nn.Module):
    """Compact CNN used for controlled imbalance experiments.

    The architecture is intentionally small so Phase 05/06 experiments can run
    repeatedly on CPU/MPS while still learning meaningful leaf-disease features.
    """

    def __init__(self, num_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 12, kernel_size=3, padding=1),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(12, 24, kernel_size=3, padding=1),
            nn.BatchNorm2d(24),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(24, 48, kernel_size=3, padding=1),
            nn.BatchNorm2d(48),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(48, 96, kernel_size=3, padding=1),
            nn.BatchNorm2d(96),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Linear(96, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)


class TinyCNN(nn.Module):
    """Very small CNN retained for quick Phase 03 baselines."""

    def __init__(self, num_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(64, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(torch.flatten(self.features(x), 1))


def get_simple_cnn(num_classes: int) -> SimpleCNN:
    """Factory for the main custom CNN."""

    return SimpleCNN(num_classes=num_classes)


def get_tiny_cnn(num_classes: int) -> TinyCNN:
    """Factory for a lightweight baseline CNN."""

    return TinyCNN(num_classes=num_classes)


def get_mobilenet_v2(
    num_classes: int,
    freeze_features: bool = True,
    dropout_p: float = 0.0,
) -> nn.Module:
    """Build MobileNetV2 with an experiment-specific classification head.

    Parameters
    ----------
    num_classes:
        Number of target classes.
    freeze_features:
        If True, freeze the pretrained feature extractor for feature extraction.
    dropout_p:
        Optional dropout before the final linear classifier. A value of 0 keeps
        the old behavior used by earlier notebooks.
    """

    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    if freeze_features:
        for parameter in model.features.parameters():
            parameter.requires_grad = False

    in_features = model.classifier[1].in_features
    if dropout_p > 0:
        model.classifier = nn.Sequential(
            nn.Dropout(p=dropout_p),
            nn.Linear(in_features, num_classes),
        )
    else:
        model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


def get_efficientnet_b0(
    num_classes: int,
    freeze_features: bool = True,
    dropout_p: float = 0.2,
) -> nn.Module:
    """Build EfficientNet-B0 with a custom classification head.

    EfficientNet-B0 is kept as the second modern pretrained model for the final
    machine-learning comparison. It is lightweight enough for this project while
    still being a strong transfer-learning baseline.
    """

    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

    if freeze_features:
        for parameter in model.features.parameters():
            parameter.requires_grad = False

    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=dropout_p),
        nn.Linear(in_features, num_classes),
    )
    return model


class ResidualBlock(nn.Module):
    """Lightweight residual block for disease-specific local textures."""

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        self.conv_path = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
        )

        if stride != 1 or in_channels != out_channels:
            self.skip_path = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.skip_path = nn.Identity()

        self.activation = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.activation(self.conv_path(x) + self.skip_path(x))


class SEBlock(nn.Module):
    """Squeeze-and-Excitation channel attention block."""

    def __init__(self, channels: int, reduction: int = 8):
        super().__init__()
        hidden_channels = max(channels // reduction, 4)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, hidden_channels),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_channels, channels),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, channels, _, _ = x.shape
        weights = self.pool(x).view(batch_size, channels)
        weights = self.fc(weights).view(batch_size, channels, 1, 1)
        return x * weights


class SpatialAttention(nn.Module):
    """Small spatial attention module used by the lightweight CBAM block."""

    def __init__(self, kernel_size: int = 7):
        super().__init__()
        padding = kernel_size // 2
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=padding, bias=False)
        self.activation = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_map = torch.mean(x, dim=1, keepdim=True)
        max_map, _ = torch.max(x, dim=1, keepdim=True)
        attention = self.activation(self.conv(torch.cat([avg_map, max_map], dim=1)))
        return x * attention


class LightweightCBAM(nn.Module):
    """Lightweight CBAM with SE-style channel attention plus spatial attention."""

    def __init__(self, channels: int, reduction: int = 8):
        super().__init__()
        self.channel_attention = SEBlock(channels=channels, reduction=reduction)
        self.spatial_attention = SpatialAttention(kernel_size=7)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.channel_attention(x)
        return self.spatial_attention(x)


class ResidualEnhancementBranch(nn.Module):
    """A shallow CNN branch for local leaf disease cues."""

    def __init__(self, attention: str | None = None, out_channels: int = 96):
        super().__init__()
        mid_channels = out_channels // 2
        self.stem = nn.Sequential(
            nn.Conv2d(3, mid_channels, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
        )
        self.block1 = ResidualBlock(mid_channels, mid_channels, stride=1)
        self.block2 = ResidualBlock(mid_channels, out_channels, stride=2)

        if attention == "se":
            self.attention = SEBlock(out_channels)
        elif attention == "cbam":
            self.attention = LightweightCBAM(out_channels)
        else:
            self.attention = nn.Identity()

        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.out_channels = out_channels

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.stem(x)
        x = self.block1(x)
        x = self.block2(x)
        x = self.attention(x)
        x = self.pool(x)
        return torch.flatten(x, 1)


class ImprovedMobileNetV2(nn.Module):
    """MobileNetV2 backbone fused with a residual enhancement branch."""

    def __init__(
        self,
        num_classes: int,
        attention: str | None = None,
        branch_channels: int = 96,
        dropout_p: float = 0.3,
        freeze_backbone: bool = True,
    ):
        super().__init__()
        backbone = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        self.backbone_features = backbone.features
        self.backbone_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.backbone_out_features = backbone.classifier[1].in_features

        self.residual_branch = ResidualEnhancementBranch(
            attention=attention,
            out_channels=branch_channels,
        )

        fusion_features = self.backbone_out_features + branch_channels
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout_p),
            nn.Linear(fusion_features, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_p),
            nn.Linear(256, num_classes),
        )

        self.set_backbone_trainable(not freeze_backbone)

    def set_backbone_trainable(self, trainable: bool) -> None:
        """Freeze or unfreeze the MobileNetV2 feature extractor."""

        for parameter in self.backbone_features.parameters():
            parameter.requires_grad = trainable

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        backbone_map = self.backbone_features(x)
        backbone_features = self.backbone_pool(backbone_map)
        backbone_features = torch.flatten(backbone_features, 1)

        residual_features = self.residual_branch(x)
        fused_features = torch.cat([backbone_features, residual_features], dim=1)
        return self.classifier(fused_features)


def get_improved_mobilenet_v2(
    num_classes: int,
    attention: str | None = None,
    branch_channels: int = 96,
    dropout_p: float = 0.3,
    freeze_backbone: bool = True,
) -> ImprovedMobileNetV2:
    """Factory for Improved-MobileNetV2 variants."""

    return ImprovedMobileNetV2(
        num_classes=num_classes,
        attention=attention,
        branch_channels=branch_channels,
        dropout_p=dropout_p,
        freeze_backbone=freeze_backbone,
    )
