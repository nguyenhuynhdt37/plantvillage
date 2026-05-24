# Phase 07 Report: Pretrained Transition Study

Phase 07 làm gọn pipeline: SimpleCNN vẫn là baseline nghiên cứu chính trong Phase 01-07, đồng thời kiểm tra nhanh MobileNetV2 pretrained để chuẩn bị cho Phase 08.

## Experiment summary
       Experiment                                                                            Strategy  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst-class Recall
    pretrained_ce                                               MobileNetV2 pretrained + CrossEntropy  0.917182         0.904280      0.900647  0.899178         0.875014            0.533333
pretrained_winner MobileNetV2 pretrained + WeightedRandomSampler + Light Augmentation + EarlyStopping  0.903585         0.874583      0.902359  0.878094         0.909184            0.666667
     simplecnn_ce                                                            SimpleCNN + CrossEntropy  0.849197         0.821779      0.799113  0.798896         0.715883            0.277778
 simplecnn_winner              SimpleCNN + WeightedRandomSampler + Light Augmentation + EarlyStopping  0.813968         0.777198      0.810419  0.776572         0.825180            0.350877

## Key interpretation
Experiment tốt nhất theo Macro F1 là `pretrained_ce` với Macro F1 = 0.8992 và Minority Recall = 0.8750.
Kết quả Phase 07 dùng để quyết định có nên chuyển sang nghiên cứu mô hình pretrained hiện đại đầy đủ ở Phase 08 hay không.