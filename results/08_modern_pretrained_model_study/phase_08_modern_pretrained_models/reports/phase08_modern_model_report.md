# Phase 08 Report: CNN Model Study

Phase 08 huấn luyện SimpleCNN, MobileNetV2 pretrained và EfficientNet-B0 pretrained trên cùng winner imbalance strategy. Mỗi experiment được giới hạn tối đa 15 epoch với EarlyStopping theo Validation Macro F1.

## Comparison
            Experiment           Model  Params  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst-class Recall
    mobilenetv2_winner     mobilenetv2 2272550  0.986559         0.980589      0.985519  0.982922         0.990943            0.936170
efficientnet_b0_winner efficientnet_b0 4056226  0.984165         0.978211      0.981341  0.979556         0.979141            0.897959
     simple_cnn_winner      simple_cnn   63974  0.942368         0.922192      0.946779  0.929444         0.974950            0.710000

## Conclusion
Mô hình tốt nhất theo Macro F1 là `mobilenetv2_winner` với Macro F1 = 0.9829, Minority Recall = 0.9909.