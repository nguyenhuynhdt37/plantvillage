# Final Project Report: PlantVillage Disease Classification
Generated at: 2026-06-02 09:10:47

## 1. Project Overview
Dự án nghiên cứu class imbalance handling, transfer learning, lightweight CNN architectures và fairness-aware plant disease classification trên PlantVillage.

## 2. Final Cross-Phase Comparison
   Phase                     Model                                                                                Strategy              Experiment  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst Recall  Params  Inference Time ms/image   Source
Phase 09 Best Improved MobileNetV2                               Best residual/attention enhanced MobileNetV2 architecture mobilenetv2_residual_se  0.991530         0.986750      0.991044  0.988808         0.994118      0.941176 2761218                      NaN Phase 09
Phase 08          Best MobileNetV2     MobileNetV2 pretrained + WeightedRandomSampler + Light Augmentation + EarlyStopping      mobilenetv2_winner  0.986559         0.980589      0.985519  0.982922         0.990943      0.936170 2272550                      NaN Phase 08
Phase 08      Best EfficientNet-B0 EfficientNet-B0 pretrained + WeightedRandomSampler + Light Augmentation + EarlyStopping  efficientnet_b0_winner  0.984165         0.978211      0.981341  0.979556         0.979141      0.897959 4056226                      NaN Phase 08
Phase 08                 SimpleCNN    SimpleCNN + WeightedRandomSampler + Light Augmentation + EarlyStopping, 15 epoch cap       simple_cnn_winner  0.942368         0.922192      0.946779  0.929444         0.974950      0.710000   63974                      NaN Phase 08

## 3. Final Results Summary
                 Category                     Model              Experiment  Macro F1  Minority Recall  Worst Recall
       Best overall model Best Improved MobileNetV2 mobilenetv2_residual_se  0.988808         0.994118      0.941176
Best fairness-aware model Best Improved MobileNetV2 mobilenetv2_residual_se  0.988808         0.994118      0.941176
   Best lightweight model                 SimpleCNN       simple_cnn_winner  0.929444         0.974950      0.710000

## 4. Research Question Analysis
                                                       Research Question                                                                                                                                             Evidence                                                                                                                                                  Interpretation
 RQ1: SimpleCNN có đủ mạnh khi dùng cùng imbalance-aware pipeline không? Phase 08 simple_cnn_winner chạy cùng WeightedRandomSampler, light augmentation, EarlyStopping và giới hạn tối đa 15 epoch như hai pretrained models.                                SimpleCNN đóng vai trò mô hình CNN tự xây dựng để làm mốc so sánh với các pretrained backbones trong cùng điều kiện thực nghiệm.
                  RQ2: MobileNetV2 cải thiện bao nhiêu so với SimpleCNN?                                                                      Best MobileNetV2 vs SimpleCNN: ΔMacro F1 = +0.0535, ΔMinority Recall = +0.0160.                                So sánh này đo giá trị tăng thêm của transfer learning so với CNN custom trong cùng split và cùng chiến lược xử lý mất cân bằng.
                         RQ3: EfficientNet-B0 có vượt MobileNetV2 không?                                                           Best EfficientNet-B0 vs Best MobileNetV2: ΔMacro F1 = -0.0034, ΔMinority Recall = -0.0118.                                                                           So sánh này chọn pretrained backbone phù hợp hơn giữa MobileNetV2 và EfficientNet-B0.
RQ4: Best Improved MobileNetV2 có outperform MobileNetV2 baseline không?                                                                     Best Improved MobileNetV2 vs Phase 09 MobileNetV2 baseline: ΔMacro F1 = +0.0059. Residual/attention enhancement chỉ nên được xem là thành công nếu cải thiện Macro F1 hoặc minority metrics tương xứng với chi phí parameters và inference time.

## 5. Statistical Analysis
                                       Comparison   Metric  N  Mean Delta  Wilcoxon p-value  Effect Size dz                                                                                        Note
                    SimpleCNN vs Best MobileNetV2   Recall 38    0.038740      7.253333e-06        0.827883 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
                    SimpleCNN vs Best MobileNetV2 F1-score 38    0.053477      4.972161e-07        0.776650 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
         Best MobileNetV2 vs Best EfficientNet-B0   Recall 38   -0.004178      1.981229e-01       -0.258362 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
         Best MobileNetV2 vs Best EfficientNet-B0 F1-score 38   -0.003366      1.243968e-01       -0.286190 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
MobileNetV2 baseline vs Best Improved MobileNetV2   Recall 38    0.005525      2.605563e-03        0.499947 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
MobileNetV2 baseline vs Best Improved MobileNetV2 F1-score 38    0.005886      1.226738e-04        0.618611 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.

## 6. Fairness and Imbalance Analysis
   Phase                     Model              Experiment  Accuracy  Macro F1  Minority Recall  Worst Recall  Accuracy - Macro F1 Gap  Minority - Worst Gap
Phase 09 Best Improved MobileNetV2 mobilenetv2_residual_se  0.991530  0.988808         0.994118      0.941176                 0.002723              0.052941
Phase 08          Best MobileNetV2      mobilenetv2_winner  0.986559  0.982922         0.990943      0.936170                 0.003637              0.054773
Phase 08      Best EfficientNet-B0  efficientnet_b0_winner  0.984165  0.979556         0.979141      0.897959                 0.004609              0.081182
Phase 08                 SimpleCNN       simple_cnn_winner  0.942368  0.929444         0.974950      0.710000                 0.012924              0.264950

## 7. Efficiency Analysis
                  Model  Total Params  Estimated Param Memory MB  Inference Time ms/image           Suitability
   mobilenetv2_baseline       2272550                   8.669090                 6.382685 Mobile/edge candidate
   mobilenetv2_residual       2758806                  10.524010                 7.698215 Mobile/edge candidate
mobilenetv2_residual_se       2761218                  10.533211                 7.989906 Mobile/edge candidate

## 8. Explainability Synthesis
 Grad-CAM artifact count                                                                                                    Grad-CAM directory                                                   Interpretation
                       4 /Users/huynh/codes/kpdl/plan/results/09_improved_mobilenetv2_architecture_study/phase_09_improved_mobilenetv2/gradcam Grad-CAM panels available for qualitative localization analysis.

## 9. Hardest-Class / Failure Case Synthesis
                    Model  Class_ID                                              Class  Train Sample Count  Is Minority   Recall  F1-score
                SimpleCNN        29                              Tomato___Early_blight                 800        False 0.710000  0.767568
                SimpleCNN         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.867347  0.909091
                SimpleCNN        28                            Tomato___Bacterial_spot                1702        False 0.873239  0.909535
                SimpleCNN        30                               Tomato___Late_blight                1527        False 0.874346  0.874346
                SimpleCNN        21                               Potato___Late_blight                 800        False 0.880000  0.880000
                SimpleCNN        11                                  Grape___Black_rot                 944        False 0.881356  0.924444
                SimpleCNN        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.904762  0.918429
                SimpleCNN        34                               Tomato___Target_Spot                1123        False 0.907801  0.870748
                SimpleCNN        18                      Pepper,_bell___Bacterial_spot                 798        False 0.909091  0.918367
                SimpleCNN        23                                Raspberry___healthy                 297         True 0.918919  0.944444
         Best MobileNetV2        34                               Tomato___Target_Spot                1123        False 0.936170  0.946237
         Best MobileNetV2        29                              Tomato___Early_blight                 800        False 0.940000  0.912621
         Best MobileNetV2         7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                 410         True 0.941176  0.923077
         Best MobileNetV2        30                               Tomato___Late_blight                1527        False 0.947644  0.960212
         Best MobileNetV2         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.948980  0.958763
         Best MobileNetV2        28                            Tomato___Bacterial_spot                1702        False 0.957746  0.973747
         Best MobileNetV2        31                                 Tomato___Leaf_Mold                 762        False 0.957895  0.957895
         Best MobileNetV2         0                                 Apple___Apple_scab                 504         True 0.968254  0.976000
         Best MobileNetV2         3                                    Apple___healthy                1316        False 0.969697  0.981595
         Best MobileNetV2        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.976190  0.973294
     Best EfficientNet-B0         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.897959  0.926316
     Best EfficientNet-B0         7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                 410         True 0.921569  0.878505
     Best EfficientNet-B0        22                                   Potato___healthy                 122         True 0.933333  0.965517
     Best EfficientNet-B0        34                               Tomato___Target_Spot                1123        False 0.936170  0.926316
     Best EfficientNet-B0         0                                 Apple___Apple_scab                 504         True 0.936508  0.959350
     Best EfficientNet-B0        29                              Tomato___Early_blight                 800        False 0.940000  0.930693
     Best EfficientNet-B0        30                               Tomato___Late_blight                1527        False 0.947644  0.965333
     Best EfficientNet-B0        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.958333  0.955490
     Best EfficientNet-B0        28                            Tomato___Bacterial_spot                1702        False 0.967136  0.976303
     Best EfficientNet-B0        12                       Grape___Esca_(Black_Measles)                1106        False 0.971223  0.981818
Best Improved MobileNetV2         7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                 410         True 0.941176  0.941176
Best Improved MobileNetV2        29                              Tomato___Early_blight                 800        False 0.950000  0.954774
Best Improved MobileNetV2        34                               Tomato___Target_Spot                1123        False 0.950355  0.957143
Best Improved MobileNetV2        28                            Tomato___Bacterial_spot                1702        False 0.967136  0.980952
Best Improved MobileNetV2         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.969388  0.969388
Best Improved MobileNetV2        11                                  Grape___Black_rot                 944        False 0.983051  0.987234
Best Improved MobileNetV2        30                               Tomato___Late_blight                1527        False 0.984293  0.981723
Best Improved MobileNetV2         3                                    Apple___healthy                1316        False 0.987879  0.993902
Best Improved MobileNetV2        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.988095  0.985163
Best Improved MobileNetV2        32                        Tomato___Septoria_leaf_spot                1417        False 0.988701  0.985915

## 10. Core Scientific Insights
 Insight_ID                                                                                                                                   Scientific Insight
          1          Phase 10 tập trung đánh giá bốn mô hình đại diện cuối cùng: SimpleCNN, Best MobileNetV2, Best EfficientNet-B0 và Best Improved MobileNetV2.
          2                                   SimpleCNN là mốc CNN custom để kiểm tra năng lực của kiến trúc tự xây dựng khi dùng cùng imbalance-aware pipeline.
          3     Best MobileNetV2 và Best EfficientNet-B0 cho phép đánh giá trực tiếp tác động của pretrained CNN backbones trong cùng điều kiện tối đa 15 epoch.
          4     Best Improved MobileNetV2 kiểm tra liệu residual branch và attention có cải thiện MobileNetV2 baseline tương xứng với chi phí mô hình hay không.
          5 Accuracy không phải metric đủ tin cậy trong severe imbalance. Macro F1, Minority Recall và Worst Recall phản ánh fairness-aware performance tốt hơn.

## 11. Limitations
                                                                                                                          Limitation
                          Một số phase có thể chỉ có single-run, nên statistical significance chưa mạnh bằng multi-seed experiments.
Một số phase trước dùng subset để nghiên cứu nhanh; Phase 08/09 dùng full data nhưng cross-phase comparison cần diễn giải cẩn trọng.
                                  PlantVillage là dataset tương đối sạch, có thể không phản ánh đầy đủ điều kiện ảnh ngoài thực địa.
                                                              Chưa có cross-dataset validation hoặc external field-image validation.
                                                                         Hyperparameter search còn giới hạn do computational budget.
                                       Grad-CAM/Grad-CAM++ là explainability định tính, không chứng minh causal reasoning của model.
                                                      Chưa so sánh với Vision Transformer hoặc self-supervised pretrained backbones.

## 12. Future Work
                                                                          Future Work
Chạy multi-seed experiments để báo cáo mean/std và statistical significance mạnh hơn.
       Thử cross-dataset validation trên dữ liệu thực địa hoặc dataset bệnh cây khác.
            So sánh thêm với Vision Transformer và self-supervised pretrained models.
            Tối ưu deployment bằng pruning, quantization hoặc knowledge distillation.
      Kết hợp disease localization/segmentation để tăng explainability và robustness.
   Đánh giá latency, memory và energy consumption trực tiếp trên mobile/edge devices.
                  Thiết kế augmentation mạnh hơn nhưng vẫn bảo toàn triệu chứng bệnh.

## 13. Final Discussion
FINAL DISCUSSION
================

Phase 10 là giai đoạn tổng hợp và đánh giá cuối cùng của dự án PlantVillage Disease Classification. Ở phase này, nhóm không huấn luyện thêm mô hình mới mà sử dụng các kết quả tốt nhất đã thu được từ các phase trước để so sánh tổng thể.

Cụ thể, Phase 10 đánh giá bốn mô hình chính: SimpleCNN, Best MobileNetV2, Best EfficientNet-B0 và Best Improved MobileNetV2. SimpleCNN đóng vai trò mô hình CNN custom đại diện, trong khi MobileNetV2 và EfficientNet-B0 đại diện cho các pretrained CNN backbones. Best Improved MobileNetV2 là mô hình cải tiến tốt nhất từ Phase 09, dùng để kiểm tra hiệu quả của residual branch và attention mechanism.

Các mô hình được so sánh dựa trên Accuracy, Macro F1, Minority Recall, Worst Recall, per-class behavior và độ phức tạp mô hình nếu artifact complexity có sẵn. Việc tập trung vào Macro F1, Minority Recall và Worst Recall giúp đánh giá công bằng hơn trong bối cảnh dữ liệu mất cân bằng, thay vì chỉ dựa vào Accuracy.

Best overall model theo Macro F1 là `Best Improved MobileNetV2` (`mobilenetv2_residual_se`) với Macro F1 = 0.9888. Best fairness-aware model theo Minority Recall/Worst Recall là `Best Improved MobileNetV2` (`mobilenetv2_residual_se`) với Minority Recall = 0.9941. Các kết quả này là cơ sở để xác định mô hình phù hợp nhất cho bài toán phân loại bệnh lá cây trên PlantVillage.

## 14. Final Conclusion
FINAL CONCLUSION
================

Phase 10 tổng hợp kết quả của SimpleCNN, Best MobileNetV2, Best EfficientNet-B0 và Best Improved MobileNetV2. Kết luận cuối cùng được rút ra từ hiệu năng tổng thể, khả năng nhận diện minority classes, worst-class behavior và trade-off giữa độ chính xác và độ phức tạp mô hình.

Trong phạm vi nghiên cứu này, mô hình được chọn cuối cùng nên là mô hình có Macro F1 cao, Minority Recall ổn định và Worst Recall tốt, thay vì chỉ có Accuracy cao trên các lớp phổ biến.