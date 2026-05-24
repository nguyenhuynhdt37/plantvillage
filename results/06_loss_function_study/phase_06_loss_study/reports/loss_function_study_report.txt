# Báo cáo Phase 06: Loss Function Study
Thời điểm tạo báo cáo: 2026-05-24 12:47:02

## 1. Methodology
Phase 06 giữ nguyên split, image size, SimpleCNN architecture, light augmentation và EarlyStopping theo Validation Macro F1 như Phase 05. Khác biệt chính giữa các thí nghiệm là loss function.

## 2. Loss functions
- CrossEntropyLoss: baseline loss không weighting.
- Weighted CrossEntropyLoss: tăng penalty cho class thiểu số bằng inverse-frequency weights.
- Focal Loss: tập trung vào hard samples bằng hệ số `(1 - pt)^gamma`.
- Class-Balanced Loss: dùng effective number of samples để tính class weights ổn định hơn.

## 3. Quantitative results
         Experiment  Accuracy  Macro Precision  Macro Recall  Macro F1  Minority Recall  Worst-class Recall
class_balanced_loss  0.832509         0.775059      0.845858  0.795935         0.886295            0.452830
         focal_loss  0.834363         0.818876      0.799888  0.795813         0.807267            0.366667
        ce_baseline  0.836218         0.798178      0.809228  0.783917         0.818854            0.266667
        weighted_ce  0.759580         0.713443      0.759937  0.710292         0.793740            0.350877

## 4. Per-class metrics
Bảng per-class Recall/F1 đầy đủ được lưu tại `tables/per_class_recall_f1_by_loss.csv`. Đây là bảng dùng để kiểm tra class nào hưởng lợi hoặc suy giảm dưới từng loss function.

## 5. Discussion
CrossEntropyLoss thường bị bias về majority classes vì phần lớn gradient đến từ các class có nhiều mẫu. Weighted CE cải thiện sensitivity với minority classes, nhưng weight quá lớn có thể làm training kém ổn định. Focal Loss chuyển trọng tâm từ easy majority samples sang hard samples, nên có tiềm năng cải thiện các class khó học. Class-Balanced Loss dựa trên effective number theory, nhờ đó xử lý imbalance mềm hơn inverse-frequency weighting thuần túy.

Experiment có Macro F1 tốt nhất là `class_balanced_loss`. Experiment có Minority Recall tốt nhất là `class_balanced_loss`. Nếu Accuracy giảm nhẹ nhưng Macro F1, Minority Recall hoặc Worst-class Recall tăng, đây là trade-off có ý nghĩa trong bối cảnh severe class imbalance.

Loss-level balancing khác sampler-based balancing: loss-level thay đổi hàm mục tiêu tối ưu, trong khi sampler-based thay đổi xác suất xuất hiện của mẫu trong mini-batch. Vì vậy hai hướng này trả lời hai câu hỏi nghiên cứu khác nhau và có thể được so sánh hoặc kết hợp ở các phase sau.

## 6. Conclusions
- Accuracy không đủ để đánh giá model trong dữ liệu mất cân bằng nghiêm trọng.
- Macro F1, Minority Recall và Worst-class Recall phản ánh tốt hơn khả năng nhận diện minority classes.
- Weighted CE và Class-Balanced Loss xử lý imbalance bằng class weights.
- Focal Loss tập trung vào hard samples và có thể hỗ trợ class khó học.
- Loss function study cung cấp góc nhìn bổ sung cho sampler/resampling study ở Phase 05.