# Phase 07 Report: SimpleCNN Hybrid Strategy Study

## 1. Hybrid design
                               Hybrid Experiment    Phase 05 Component                                       Phase 05 Description  Phase 06 Component  Train Size  Use Sampler  Use EarlyStopping
hybrid_sampler_aug_earlystop_class_balanced_loss sampler_aug_earlystop WeightedRandomSampler + Light Augmentation + EarlyStopping class_balanced_loss        9383         True               True

## 2. Hybrid vs individual winners
         Source                                       Experiment                                    Strategy  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst Recall
Phase 05 Winner                            sampler_aug_earlystop                       sampler_aug_earlystop  0.833127              NaN           NaN  0.812635         0.898826      0.522727
Phase 06 Winner                              class_balanced_loss                         class_balanced_loss  0.832509         0.775059      0.845858  0.795935         0.886295      0.452830
Phase 07 Hybrid hybrid_sampler_aug_earlystop_class_balanced_loss sampler_aug_earlystop + class_balanced_loss  0.736712         0.735455      0.792523  0.727835         0.891028      0.396226

## 3. Interpretation
PHASE 07 INTERPRETATION
=======================

Phase 07 kiểm tra hybrid strategy bằng SimpleCNN: kết hợp winner của Phase 05 (`sampler_aug_earlystop`) với winner của Phase 06 (`class_balanced_loss`).

Kết quả so sánh:
- Hybrid ΔMacro F1 so với Phase 05 winner: -0.0848
- Hybrid ΔMacro F1 so với Phase 06 winner: -0.0681

Experiment tốt nhất theo Macro F1 là `sampler_aug_earlystop` từ `Phase 05 Winner` với Macro F1 = 0.8126.

Hybrid strategy không vượt winner đơn lẻ. Điều này cho thấy một hướng imbalance handling đã đủ mạnh hoặc việc kết hợp làm optimization kém ổn định hơn.

Phase 07 vẫn thuộc giai đoạn SimpleCNN. Từ Phase 08 trở đi mới bắt đầu huấn luyện các mô hình học sâu hiện đại như MobileNetV2 và EfficientNet-B0.