# Phase 11: Model Architecture Inspection

Phase này kiểm tra cấu trúc 3 nhóm model chính của đồ án: SimpleCNN, MobileNetV2 và EfficientNet-B0. Notebook không train model và dùng `weights=None` cho model torchvision để tránh phụ thuộc pretrained download.

## Parameter Summary

          model   model_type  total_parameters  trainable_parameters
     simple_cnn    SimpleCNN             63974                 63974
    mobilenetv2  MobileNetV2           2272550               2272550
efficientnet_b0 EfficientNet           4056226               4056226

## SimpleCNN features

[0] Conv2d
[1] BatchNorm2d
[2] ReLU
[3] MaxPool2d
[4] Conv2d
[5] BatchNorm2d
[6] ReLU
[7] MaxPool2d
[8] Conv2d
[9] BatchNorm2d
[10] ReLU
[11] MaxPool2d
[12] Conv2d
[13] BatchNorm2d
[14] ReLU
[15] AdaptiveAvgPool2d

SimpleCNN là baseline tự xây dựng, có feature extractor nhỏ gồm các tầng convolution, batch normalization, ReLU, pooling và classifier MLP. Vai trò của SimpleCNN là baseline kiểm soát trước khi chuyển sang pretrained backbone.

## MobileNetV2 features

[0] ConvBNActivation
[1] InvertedResidual
[2] InvertedResidual
[3] InvertedResidual
[4] InvertedResidual
[5] InvertedResidual
[6] InvertedResidual
[7] InvertedResidual
[8] InvertedResidual
[9] InvertedResidual
[10] InvertedResidual
[11] InvertedResidual
[12] InvertedResidual
[13] InvertedResidual
[14] InvertedResidual
[15] InvertedResidual
[16] InvertedResidual
[17] InvertedResidual
[18] ConvBNActivation

MobileNetV2 gồm 19 top-level blocks trong `features`. Các block `[1]` đến `[17]` là `InvertedResidual`, đây là phần cốt lõi của MobileNetV2. Block đầu và cuối là convolution + normalization + activation; trong torchvision mới tên là `Conv2dNormActivation`, có thể ghi ngắn trong báo cáo là `ConvBNActivation` hoặc `ConvBNReLU6`.

## EfficientNet-B0 features

[0] ConvBNActivation
[1] Sequential
[2] Sequential
[3] Sequential
[4] Sequential
[5] Sequential
[6] Sequential
[7] Sequential
[8] ConvBNActivation

EfficientNet-B0 có feature extractor theo các stage EfficientNet, gồm stem convolution, các nhóm MBConv/FusedMBConv và final convolution block. Model này được dùng ở Phase 08 để so sánh với MobileNetV2 trong nhóm pretrained CNN hiện đại.

## Ý nghĩa phân tích

SimpleCNN nhỏ và dễ kiểm soát nhưng năng lực biểu diễn thấp hơn pretrained backbones. MobileNetV2 dùng inverted residual bottleneck nên nhẹ và phù hợp mobile/edge. EfficientNet-B0 dùng thiết kế EfficientNet với scaling cân bằng depth/width/resolution, thường mạnh hơn nhưng cấu trúc phức tạp hơn. Việc inspect 3 model giúp giải thích vì sao Phase 08 chuyển từ baseline tự xây dựng sang pretrained backbone hiện đại.
