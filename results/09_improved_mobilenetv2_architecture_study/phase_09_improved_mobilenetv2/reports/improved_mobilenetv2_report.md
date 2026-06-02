# Báo cáo Phase 09: Improved MobileNetV2 Architecture Study
Thời điểm tạo báo cáo: 2026-06-01 23:56:01

## 1. Architecture design
- Path 1: MobileNetV2 pretrained backbone làm feature extractor chính.
- Path 2: residual enhancement branch học local disease textures.
- Attention: SE block hoặc lightweight CBAM để tăng khả năng focus vùng bệnh.
- Fusion: concatenate backbone features và residual features, sau đó qua classifier head.

## 2. Methodology
Tất cả model dùng WeightedRandomSampler, Light Augmentation và EarlyStopping theo Validation Macro F1. Training theo two-stage transfer learning: feature extraction rồi fine-tuning.

## 3. Ablation study
                  Model  Params  Accuracy  Macro F1  Macro Precision  Macro Recall  Minority Recall  Worst Recall
mobilenetv2_residual_se 2761218  0.991530  0.988808         0.986750      0.991044         0.994118      0.941176
   mobilenetv2_residual 2758806  0.990978  0.988389         0.986201      0.990837         0.994865      0.940000
   mobilenetv2_baseline 2272550  0.986559  0.982922         0.980589      0.985519         0.990943      0.936170

## 4. Model complexity
                  Model  Total Params  Trainable Params Stage 1  Estimated Param Memory MB  Inference Time ms/image
   mobilenetv2_baseline       2272550                     48678                   8.669090                 6.382685
   mobilenetv2_residual       2758806                    534934                  10.524010                 7.698215
mobilenetv2_residual_se       2761218                    537346                  10.533211                 7.989906

## 5. Per-class and error analysis
Per-class Recall/F1, hardest-class ranking và misclassification histogram được lưu trong thư mục `tables/`.

## 6. Explainability analysis
Grad-CAM và Grad-CAM++ visualizations được lưu trong thư mục `gradcam/`. Các heatmap dùng để kiểm tra model có tập trung vào vùng bệnh trên lá hay không.

## 7. Discussion
THẢO LUẬN HỌC THUẬT
===================

Phase 09 đề xuất Improved-MobileNetV2 bằng cách kết hợp MobileNetV2 pretrained backbone với residual enhancement branch và attention nhẹ. MobileNetV2 cung cấp feature extractor mạnh, học được các visual primitives từ ImageNet. Residual branch được thiết kế nông và nhẹ để học thêm local disease patterns như đốm bệnh, texture tổn thương và biến đổi màu sắc trên lá.

SE attention hoặc CBAM nhẹ có mục tiêu giúp model tăng trọng số cho các kênh hoặc vùng không gian có thông tin phân biệt bệnh. Điều này đặc biệt quan trọng trong plant disease classification vì vùng bệnh có thể nhỏ, không nằm ở trung tâm ảnh hoặc bị nhiễu bởi nền lá khỏe.

Best architecture là `mobilenetv2_residual_se` với Macro F1 = 0.9888, Minority Recall = 0.9941, Worst Recall = 0.9412. So với MobileNetV2 baseline, Macro F1 thay đổi +0.0059, Minority Recall thay đổi +0.0032, và số parameters thay đổi +488,668.

Improved architecture cho thấy hiệu quả bổ trợ: tăng đồng thời Macro F1 và Minority Recall so với MobileNetV2 baseline.

Về deployment, kiến trúc cải tiến vẫn giữ MobileNetV2 làm backbone chính và residual branch tương đối nhỏ. Vì vậy mô hình vẫn phù hợp hơn cho edge/mobile deployment so với các backbone lớn. Tuy nhiên, nếu số parameters hoặc inference time tăng mà Macro F1 không cải thiện tương ứng, kiến trúc baseline vẫn là lựa chọn hiệu quả hơn.

## 8. Conclusions
- MobileNetV2 pretrained là backbone mạnh cho PlantVillage classification.
- Residual enhancement branch có mục tiêu bổ sung local disease texture learning.
- SE/CBAM attention giúp kiểm tra vai trò focus vào disease-discriminative regions.
- WeightedRandomSampler vẫn quan trọng để cải thiện minority exposure.
- Kiến trúc cải tiến chỉ nên được chọn nếu cải thiện Macro F1/Minority Recall tương xứng với chi phí parameters và inference time.