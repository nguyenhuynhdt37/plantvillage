# Phase 08 Report: Modern Pretrained Model Study

Phase 08 huấn luyện hai mô hình học sâu hiện đại chính của đồ án: MobileNetV2 pretrained và EfficientNet-B0 pretrained.

## Comparison
            Experiment           Model  Params  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst-class Recall
    mobilenetv2_winner     mobilenetv2 2272550  0.986559         0.980589      0.985519  0.982922         0.990943            0.936170
efficientnet_b0_winner efficientnet_b0 4056226  0.984165         0.978211      0.981341  0.979556         0.979141            0.897959

## Conclusion
Mô hình tốt nhất theo Macro F1 là `mobilenetv2_winner` với Macro F1 = 0.9829, Minority Recall = 0.9909.