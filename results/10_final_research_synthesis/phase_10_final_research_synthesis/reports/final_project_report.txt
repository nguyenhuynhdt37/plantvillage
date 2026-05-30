# Final Project Report: PlantVillage Disease Classification
Generated at: 2026-05-30 13:58:36

## 1. Project Overview
Dự án nghiên cứu class imbalance handling, transfer learning, lightweight CNN architectures và fairness-aware plant disease classification trên PlantVillage.

## 2. Final Cross-Phase Comparison
   Phase                            Model                                                   Strategy              Experiment  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst Recall    Params  Inference Time ms/image   Source
Phase 09 Improved MobileNetV2 final model                    Residual/attention enhanced MobileNetV2 mobilenetv2_residual_se  0.991530         0.986750      0.991044  0.988808         0.994118      0.941176 2761218.0                      NaN Phase 09
Phase 08               MobileNetV2 winner           MobileNetV2 pretrained + sampler winner strategy      mobilenetv2_winner  0.986559         0.980589      0.985519  0.982922         0.990943      0.936170 2272550.0                      NaN Phase 08
Phase 08           EfficientNet-B0 winner       EfficientNet-B0 pretrained + sampler winner strategy  efficientnet_b0_winner  0.984165         0.978211      0.981341  0.979556         0.979141      0.897959 4056226.0                      NaN Phase 08
Phase 05                  Phase 05 winner WeightedRandomSampler + Light Augmentation + EarlyStopping   sampler_aug_earlystop  0.833127              NaN           NaN  0.812635         0.898826      0.522727       NaN                      NaN Phase 05
Phase 07        SimpleCNN hybrid strategy                Best Phase 05 strategy + best Phase 06 loss   sampler_aug_earlystop  0.833127              NaN           NaN  0.812635         0.898826      0.522727       NaN                      NaN Phase 07
Phase 05               SimpleCNN baseline                                      CrossEntropy baseline                baseline  0.849197              NaN           NaN  0.798896         0.715883      0.277778       NaN                      NaN Phase 05
Phase 06        Best loss-level SimpleCNN                   Best loss function strategy on SimpleCNN     class_balanced_loss  0.832509         0.775059      0.845858  0.795935         0.886295      0.452830       NaN                      NaN Phase 06

## 3. Final Results Summary
                 Category                            Model              Experiment  Macro F1  Minority Recall  Worst Recall
       Best overall model Improved MobileNetV2 final model mobilenetv2_residual_se  0.988808         0.994118      0.941176
Best fairness-aware model Improved MobileNetV2 final model mobilenetv2_residual_se  0.988808         0.994118      0.941176
   Best lightweight model                  Phase 05 winner   sampler_aug_earlystop  0.812635         0.898826      0.522727

## 4. Research Question Analysis
                                                                  Research Question                                                                                                                          Evidence                                                                                                                                                                               Interpretation
                   RQ1: Imbalance handling có cải thiện minority recognition không?                                      Phase 05 sampler_aug_earlystop vs baseline: ΔMinority Recall = +0.1829, ΔMacro F1 = +0.0137.                                               Sampler-based exposure, light augmentation và EarlyStopping thường cải thiện khả năng nhận diện minority classes, dù Accuracy có thể giảm nhẹ.
                   RQ2: Loss balancing có outperform sampler-based balancing không?                                                                       Best Phase 06 loss vs Phase 05 winner: ΔMacro F1 = -0.0167.                                         Loss-level balancing thay đổi objective, nhưng không luôn vượt sampler-based balancing; hiệu quả phụ thuộc mức imbalance và độ ổn định optimization.
RQ3: Hybrid strategy giữa best sampler và best loss có vượt các hướng đơn lẻ không? Phase 07 train một SimpleCNN hybrid bằng cách kết hợp winner Phase 05 với winner Phase 06, sau đó so sánh với từng winner đơn lẻ. Nếu hybrid vượt hai winner đơn lẻ, sampler/data-level balancing và loss-level balancing có hiệu ứng bổ trợ. Nếu không, một hướng đơn lẻ đã đủ mạnh hoặc hybrid gây optimization instability.
                       RQ4: MobileNetV2 và EfficientNet-B0 mô hình nào phù hợp hơn?                           Phase 08 efficientnet_b0_winner vs mobilenetv2_winner: ΔMacro F1 = -0.0034, ΔMinority Recall = -0.0118.                                                                    So sánh này trực tiếp đáp ứng yêu cầu đồ án: dùng ít nhất hai mô hình học sâu hiện đại và giải thích mô hình nào tốt hơn.
                RQ5: Improved MobileNetV2 có outperform baseline MobileNetV2 không?                                               Best Phase 09 improved model vs Phase 09 MobileNetV2 baseline: ΔMacro F1 = +0.0059.                                         Residual/attention enhancement chỉ nên được xem là thành công nếu tăng Macro F1/Minority Recall tương xứng với chi phí parameters và inference time.

## 5. Statistical Analysis
                                     Comparison   Metric  N  Mean Delta  Wilcoxon p-value  Effect Size dz                                                                                        Note
   MobileNetV2 winner vs EfficientNet-B0 winner   Recall 38   -0.004178          0.198123       -0.258362 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
   MobileNetV2 winner vs EfficientNet-B0 winner F1-score 38   -0.003366          0.124397       -0.286190 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
MobileNetV2 baseline vs mobilenetv2_residual_se   Recall 38    0.005525          0.002606        0.499947 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.
MobileNetV2 baseline vs mobilenetv2_residual_se F1-score 38    0.005886          0.000123        0.618611 Single-run paired per-class analysis; not a substitute for multi-seed significance testing.

## 6. Fairness and Imbalance Analysis
   Phase                            Model              Experiment  Accuracy  Macro F1  Minority Recall  Worst Recall  Accuracy - Macro F1 Gap  Minority - Worst Gap
Phase 09 Improved MobileNetV2 final model mobilenetv2_residual_se  0.991530  0.988808         0.994118      0.941176                 0.002723              0.052941
Phase 08               MobileNetV2 winner      mobilenetv2_winner  0.986559  0.982922         0.990943      0.936170                 0.003637              0.054773
Phase 08           EfficientNet-B0 winner  efficientnet_b0_winner  0.984165  0.979556         0.979141      0.897959                 0.004609              0.081182
Phase 05                  Phase 05 winner   sampler_aug_earlystop  0.833127  0.812635         0.898826      0.522727                 0.020492              0.376098
Phase 07        SimpleCNN hybrid strategy   sampler_aug_earlystop  0.833127  0.812635         0.898826      0.522727                 0.020492              0.376098
Phase 06        Best loss-level SimpleCNN     class_balanced_loss  0.832509  0.795935         0.886295      0.452830                 0.036574              0.433465
Phase 05               SimpleCNN baseline                baseline  0.849197  0.798896         0.715883      0.277778                 0.050300              0.438105

## 7. Efficiency Analysis
                  Model  Total Params  Estimated Param Memory MB  Inference Time ms/image           Suitability
   mobilenetv2_baseline       2272550                   8.669090                 6.649433 Mobile/edge candidate
   mobilenetv2_residual       2758806                  10.524010                 7.600310 Mobile/edge candidate
mobilenetv2_residual_se       2761218                  10.533211                 8.172040 Mobile/edge candidate

## 8. Explainability Synthesis
 Grad-CAM artifact count                                                                                                    Grad-CAM directory                                                   Interpretation
                       4 /Users/huynh/codes/kpdl/plan/results/09_improved_mobilenetv2_architecture_study/phase_09_improved_mobilenetv2/gradcam Grad-CAM panels available for qualitative localization analysis.

## 9. Hardest-Class / Failure Case Synthesis
                          Model  Class_ID                                              Class  Train Sample Count  Is Minority   Recall  F1-score
                Phase 05 winner        19                             Pepper,_bell___healthy                 236        False 0.522727  0.676471
                Phase 05 winner        16                             Peach___Bacterial_spot                 367        False 0.550725  0.612903
                Phase 05 winner         0                                 Apple___Apple_scab                 100         True 0.555556  0.588235
                Phase 05 winner        30                               Tomato___Late_blight                 305        False 0.561404  0.646465
                Phase 05 winner        32                        Tomato___Septoria_leaf_spot                 283        False 0.584906  0.596154
                Phase 05 winner        29                              Tomato___Early_blight                 160        False 0.633333  0.745098
                Phase 05 winner         3                                    Apple___healthy                 263        False 0.693878  0.731183
                Phase 05 winner        21                               Potato___Late_blight                 160        False 0.733333  0.709677
                Phase 05 winner        31                                 Tomato___Leaf_Mold                 152         True 0.750000  0.700000
                Phase 05 winner        28                            Tomato___Bacterial_spot                 340        False 0.793651  0.806452
    Phase 08 MobileNetV2 winner        34                               Tomato___Target_Spot                1123        False 0.936170  0.946237
    Phase 08 MobileNetV2 winner        29                              Tomato___Early_blight                 800        False 0.940000  0.912621
    Phase 08 MobileNetV2 winner         7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                 410         True 0.941176  0.923077
    Phase 08 MobileNetV2 winner        30                               Tomato___Late_blight                1527        False 0.947644  0.960212
    Phase 08 MobileNetV2 winner         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.948980  0.958763
    Phase 08 MobileNetV2 winner        28                            Tomato___Bacterial_spot                1702        False 0.957746  0.973747
    Phase 08 MobileNetV2 winner        31                                 Tomato___Leaf_Mold                 762        False 0.957895  0.957895
    Phase 08 MobileNetV2 winner         0                                 Apple___Apple_scab                 504         True 0.968254  0.976000
    Phase 08 MobileNetV2 winner         3                                    Apple___healthy                1316        False 0.969697  0.981595
    Phase 08 MobileNetV2 winner        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.976190  0.973294
Phase 08 EfficientNet-B0 winner         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.897959  0.926316
Phase 08 EfficientNet-B0 winner         7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                 410         True 0.921569  0.878505
Phase 08 EfficientNet-B0 winner        22                                   Potato___healthy                 122         True 0.933333  0.965517
Phase 08 EfficientNet-B0 winner        34                               Tomato___Target_Spot                1123        False 0.936170  0.926316
Phase 08 EfficientNet-B0 winner         0                                 Apple___Apple_scab                 504         True 0.936508  0.959350
Phase 08 EfficientNet-B0 winner        29                              Tomato___Early_blight                 800        False 0.940000  0.930693
Phase 08 EfficientNet-B0 winner        30                               Tomato___Late_blight                1527        False 0.947644  0.965333
Phase 08 EfficientNet-B0 winner        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.958333  0.955490
Phase 08 EfficientNet-B0 winner        28                            Tomato___Bacterial_spot                1702        False 0.967136  0.976303
Phase 08 EfficientNet-B0 winner        12                       Grape___Esca_(Black_Measles)                1106        False 0.971223  0.981818
           Improved MobileNetV2         7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                 410         True 0.941176  0.941176
           Improved MobileNetV2        29                              Tomato___Early_blight                 800        False 0.950000  0.954774
           Improved MobileNetV2        34                               Tomato___Target_Spot                1123        False 0.950355  0.957143
           Improved MobileNetV2        28                            Tomato___Bacterial_spot                1702        False 0.967136  0.980952
           Improved MobileNetV2         9                Corn_(maize)___Northern_Leaf_Blight                 788        False 0.969388  0.969388
           Improved MobileNetV2        11                                  Grape___Black_rot                 944        False 0.983051  0.987234
           Improved MobileNetV2        30                               Tomato___Late_blight                1527        False 0.984293  0.981723
           Improved MobileNetV2         3                                    Apple___healthy                1316        False 0.987879  0.993902
           Improved MobileNetV2        33      Tomato___Spider_mites Two-spotted_spider_mite                1341        False 0.988095  0.985163
           Improved MobileNetV2        32                        Tomato___Septoria_leaf_spot                1417        False 0.988701  0.985915

## 10. Core Scientific Insights
 Insight_ID                                                                                                                                                                                                  Scientific Insight
          1 Minority exposure là yếu tố trung tâm trong severe class imbalance. WeightedRandomSampler cải thiện cơ hội xuất hiện của minority samples trong mini-batch, qua đó thường làm tăng Minority Recall và Worst Recall.
          2            Loss-level balancing không nhất thiết vượt sampler-based balancing. Weighted CE, Focal Loss và Class-Balanced Loss thay đổi optimization objective, nhưng có thể gây instability nếu weighting quá mạnh.
          3                                                                  Phase 07 kiểm tra hybrid SimpleCNN: kết hợp winner sampler/data-level của Phase 05 với winner loss-level của Phase 06 để đánh giá hiệu ứng bổ trợ.
          4                                                         Phase 08 trực tiếp đáp ứng yêu cầu dùng hai mô hình học sâu hiện đại bằng cách so sánh MobileNetV2 và EfficientNet-B0 trong cùng winner imbalance strategy.
          5                                                  Improved MobileNetV2 chỉ nên được chọn nếu residual/attention enhancement cải thiện Macro F1 hoặc Minority Recall tương xứng với chi phí parameter/inference time.
          6                                                                Accuracy không phải metric đủ tin cậy trong severe imbalance. Macro F1, Minority Recall và Worst Recall phản ánh fairness-aware performance tốt hơn.

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

Dự án PlantVillage Disease Classification được triển khai như một chuỗi nghiên cứu có cấu trúc, bắt đầu từ dữ liệu và SimpleCNN baseline, mở rộng sang sampler-based imbalance handling, loss-level balancing, SimpleCNN hybrid strategy, modern transfer learning và cuối cùng là kiến trúc MobileNetV2 cải tiến. Kết quả tổng hợp cho thấy severe class imbalance không thể được đánh giá chỉ bằng Accuracy. Các metric như Macro F1, Minority Recall và Worst Recall cung cấp góc nhìn công bằng hơn về khả năng nhận diện bệnh hiếm.

Phase 05 cho thấy sampler-based balancing, đặc biệt WeightedRandomSampler kết hợp light augmentation và EarlyStopping theo Validation Macro F1, là một chiến lược hiệu quả để tăng minority exposure. Phase 06 chỉ ra rằng loss-level balancing có giá trị nghiên cứu, nhưng không mặc định vượt sampler-based balancing. Phase 07 kết hợp winner của Phase 05 và Phase 06 trong một SimpleCNN hybrid experiment để kiểm tra liệu sampler/data-level balancing và loss-level balancing có bổ trợ nhau hay không. MobileNetV2/EfficientNet-B0 chỉ bắt đầu từ Phase 08.

Phase 08 là phase huấn luyện chính cho hai mô hình học sâu hiện đại: MobileNetV2 pretrained và EfficientNet-B0 pretrained. Cả hai được đánh giá trên cùng split, cùng augmentation, cùng WeightedRandomSampler và cùng EarlyStopping để so sánh công bằng. Phase 09 tiếp tục kiểm tra liệu residual enhancement và attention mechanism có cải thiện MobileNetV2 baseline hay không, đồng thời xem xét trade-off giữa performance và computational efficiency.

Best overall model theo Macro F1 là `Improved MobileNetV2 final model` (`mobilenetv2_residual_se`) với Macro F1 = 0.9888. Best fairness-aware model theo Minority Recall/Worst Recall là `Improved MobileNetV2 final model` (`mobilenetv2_residual_se`) với Minority Recall = 0.9941. Các kết quả này nhấn mạnh rằng mô hình cuối không chỉ cần Accuracy cao mà còn phải ổn định trên minority classes.

Nhìn chung, project cho thấy modern pretrained CNN backbones và imbalance-aware training là hai thành phần bổ trợ quan trọng. MobileNetV2/EfficientNet-B0-based pipeline là hướng phù hợp cho yêu cầu đồ án học máy vì vừa có so sánh mô hình học sâu hiện đại, vừa có phân tích lỗi, imbalance và fairness-aware metrics.

## 14. Final Conclusion
FINAL CONCLUSION
================

Nghiên cứu này xây dựng một pipeline đầy đủ cho PlantVillage Disease Classification dưới severe class imbalance. Các kết quả cho thấy WeightedRandomSampler và light augmentation cải thiện minority exposure; loss-level balancing cung cấp một hướng tối ưu hóa bổ sung nhưng cần kiểm soát độ ổn định; Phase 07 kiểm tra hybrid SimpleCNN trước khi mở rộng; Phase 08 so sánh trực tiếp MobileNetV2 và EfficientNet-B0 như hai mô hình học sâu hiện đại; và Phase 09 đánh giá khả năng cải tiến MobileNetV2 bằng residual/attention enhancement.

Kết luận cuối cùng là modern pretrained CNN backbone kết hợp imbalance-aware training là final proposed direction phù hợp nhất cho bài toán fairness-aware plant disease classification trong project này.