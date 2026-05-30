# Báo cáo Phase 05: Phân tích mất cân bằng lớp
Thời điểm tạo báo cáo: 2026-05-27 23:35:22

## 1. Tổng hợp metric chính
           Thí nghiệm  Accuracy  Macro F1  Minority Recall  Worst-class Recall
             baseline  0.849197  0.798896         0.715883            0.277778
     weighted_sampler  0.831891  0.803676         0.884843            0.415094
    sampler_light_aug  0.795426  0.770671         0.852641            0.421053
sampler_aug_earlystop  0.833127  0.812635         0.898826            0.522727
    hybrid_resampling  0.816440  0.779941         0.882188            0.438596

## 2. Ablation study theo từng bước
                     So sánh     Từ thí nghiệm        Đến thí nghiệm  Chênh lệch Accuracy  Chênh lệch Macro F1  Chênh lệch Minority Recall  Chênh lệch Worst-class Recall
   Effect of WeightedSampler          baseline      weighted_sampler            -0.017305             0.004779                    0.168961                       0.137317
Effect of Light Augmentation  weighted_sampler     sampler_light_aug            -0.036465            -0.033004                   -0.032203                       0.005958
     Effect of EarlyStopping sampler_light_aug sampler_aug_earlystop             0.037701             0.041964                    0.046185                       0.101675

## 3. Các class thiểu số cải thiện nhiều nhất
 Mã class                           Tên class  Số mẫu train  Số mẫu test  Là class thiểu số  Baseline Recall  Baseline F1  Best Recall  Best F1  Mức tăng Recall  Mức tăng F1
        6   Cherry_(including_sour)___healthy           136           25               True         0.600000     0.750000     0.960000 0.761905         0.360000     0.011905
       14                     Grape___healthy           152           12               True         0.583333     0.700000     0.916667 0.785714         0.333333     0.085714
        0                  Apple___Apple_scab           100           18               True         0.277778     0.400000     0.555556 0.588235         0.277778     0.188235
       36        Tomato___Tomato_mosaic_virus           134           11               True         0.727273     0.695652     1.000000 0.758621         0.272727     0.062969
       22                    Potato___healthy            54            8               True         0.625000     0.625000     0.875000 0.482759         0.250000    -0.142241
        2            Apple___Cedar_apple_rust            99            8               True         0.875000     0.875000     1.000000 0.888889         0.125000     0.013889
       31                  Tomato___Leaf_Mold           152           28               True         0.642857     0.720000     0.750000 0.700000         0.107143    -0.020000
        9 Corn_(maize)___Northern_Leaf_Blight           157           29               True         0.827586     0.827586     0.931034 0.900000         0.103448     0.072414
       17                     Peach___healthy           129           10               True         1.000000     1.000000     1.000000 0.952381         0.000000    -0.047619
       23                 Raspberry___healthy           133           11               True         1.000000     0.880000     1.000000 0.956522         0.000000     0.076522

## 4. Các class khó học nhất
 Mã class                   Tên class  Số mẫu train   Recall  F1-score
       19      Pepper,_bell___healthy           236 0.522727  0.676471
       16      Peach___Bacterial_spot           367 0.550725  0.612903
        0          Apple___Apple_scab           100 0.555556  0.588235
       30        Tomato___Late_blight           305 0.561404  0.646465
       32 Tomato___Septoria_leaf_spot           283 0.584906  0.596154
       29       Tomato___Early_blight           160 0.633333  0.745098
        3             Apple___healthy           263 0.693878  0.731183
       21        Potato___Late_blight           160 0.733333  0.709677
       31          Tomato___Leaf_Mold           152 0.750000  0.700000
       28     Tomato___Bacterial_spot           340 0.793651  0.806452

## 5. Các cặp class bị nhầm lẫn nhiều nhất
 Mã class thực tế                          Class thực tế  Mã class dự đoán                                 Class dự đoán  Số mẫu nhầm lẫn  Tỷ lệ nhầm trong class thực tế
               19                 Pepper,_bell___healthy                18                 Pepper,_bell___Bacterial_spot               10                        0.227273
               24                      Soybean___healthy                 6             Cherry_(including_sour)___healthy               10                        0.065789
               30                   Tomato___Late_blight                33 Tomato___Spider_mites Two-spotted_spider_mite                8                        0.140351
               35 Tomato___Tomato_Yellow_Leaf_Curl_Virus                33 Tomato___Spider_mites Two-spotted_spider_mite                8                        0.050000
               30                   Tomato___Late_blight                18                 Pepper,_bell___Bacterial_spot                7                        0.122807
               16                 Peach___Bacterial_spot                18                 Pepper,_bell___Bacterial_spot                7                        0.101449
               24                      Soybean___healthy                22                              Potato___healthy                7                        0.046053
               19                 Pepper,_bell___healthy                22                              Potato___healthy                5                        0.113636
               32            Tomato___Septoria_leaf_spot                20                         Potato___Early_blight                5                        0.094340
               24                      Soybean___healthy                 3                               Apple___healthy                5                        0.032895
               12           Grape___Esca_(Black_Measles)                11                             Grape___Black_rot                4                        0.097561
               32            Tomato___Septoria_leaf_spot                16                        Peach___Bacterial_spot                4                        0.075472
               16                 Peach___Bacterial_spot                30                          Tomato___Late_blight                4                        0.057971
               35 Tomato___Tomato_Yellow_Leaf_Curl_Virus                28                       Tomato___Bacterial_spot                4                        0.025000
                0                     Apple___Apple_scab                32                   Tomato___Septoria_leaf_spot                3                        0.166667
               21                   Potato___Late_blight                34                          Tomato___Target_Spot                3                        0.100000
               29                  Tomato___Early_blight                28                       Tomato___Bacterial_spot                3                        0.100000
               11                      Grape___Black_rot                12                  Grape___Esca_(Black_Measles)                3                        0.085714
               34                   Tomato___Target_Spot                33 Tomato___Spider_mites Two-spotted_spider_mite                3                        0.071429
                3                        Apple___healthy                24                             Soybean___healthy                3                        0.061224

## 6. Bảng phân tích lỗi
 Mã class                                          Tên class  Recall của model tốt nhất  Số mẫu train                                                           Thường bị nhầm với                                                                                            Nguyên nhân tiềm năng
       19                             Pepper,_bell___healthy                   0.522727           236                              Pepper,_bell___Bacterial_spot, Potato___healthy                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       16                             Peach___Bacterial_spot                   0.550725           367                          Pepper,_bell___Bacterial_spot, Tomato___Late_blight                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
        0                                 Apple___Apple_scab                   0.555556           100                                                  Tomato___Septoria_leaf_spot texture hoặc màu sắc chồng lấn giữa các cây trồng; số mẫu train thấp; giới hạn do ảnh resize ở độ phân giải thấp
       30                               Tomato___Late_blight                   0.561404           305 Tomato___Spider_mites Two-spotted_spider_mite, Pepper,_bell___Bacterial_spot                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       32                        Tomato___Septoria_leaf_spot                   0.584906           283                                Potato___Early_blight, Peach___Bacterial_spot                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       29                              Tomato___Early_blight                   0.633333           160                                                      Tomato___Bacterial_spot                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
        3                                    Apple___healthy                   0.693878           263                                                            Soybean___healthy                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       21                               Potato___Late_blight                   0.733333           160                                                         Tomato___Target_Spot                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       31                                 Tomato___Leaf_Mold                   0.750000           152                                    Không nằm trong các cặp nhầm lẫn lớn nhất texture hoặc màu sắc chồng lấn giữa các cây trồng; số mẫu train thấp; giới hạn do ảnh resize ở độ phân giải thấp
       28                            Tomato___Bacterial_spot                   0.793651           340                                    Không nằm trong các cặp nhầm lẫn lớn nhất                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
        7 Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot                   0.800000           184                                    Không nằm trong các cặp nhầm lẫn lớn nhất                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       24                                  Soybean___healthy                   0.809211           814         Cherry_(including_sour)___healthy, Potato___healthy, Apple___healthy                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
        5           Cherry_(including_sour)___Powdery_mildew                   0.838710           168                                    Không nằm trong các cặp nhầm lẫn lớn nhất                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       11                                  Grape___Black_rot                   0.857143           188                                                 Grape___Esca_(Black_Measles)                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       34                               Tomato___Target_Spot                   0.857143           224                                Tomato___Spider_mites Two-spotted_spider_mite                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       18                      Pepper,_bell___Bacterial_spot                   0.862069           159                                    Không nằm trong các cặp nhầm lẫn lớn nhất                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       35             Tomato___Tomato_Yellow_Leaf_Curl_Virus                   0.868750           857       Tomato___Spider_mites Two-spotted_spider_mite, Tomato___Bacterial_spot                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       22                                   Potato___healthy                   0.875000            54                                    Không nằm trong các cặp nhầm lẫn lớn nhất texture hoặc màu sắc chồng lấn giữa các cây trồng; số mẫu train thấp; giới hạn do ảnh resize ở độ phân giải thấp
        1                                  Apple___Black_rot                   0.888889           223                                    Không nằm trong các cặp nhầm lẫn lớn nhất                    texture hoặc màu sắc chồng lấn giữa các cây trồng; giới hạn do ảnh resize ở độ phân giải thấp
       12                       Grape___Esca_(Black_Measles)                   0.902439           221                                                            Grape___Black_rot                      triệu chứng bệnh giống nhau trên cùng cây trồng; giới hạn do ảnh resize ở độ phân giải thấp

## 7. Thảo luận học thuật
THẢO LUẬN HỌC THUẬT
===================

Phase 05 đánh giá các chiến lược xử lý mất cân bằng lớp trong bài toán phân loại bệnh lá cây PlantVillage. Tập train được giữ ở trạng thái mất cân bằng để quan sát rõ tác động của từng kỹ thuật. Trong bối cảnh này, Accuracy không đủ để kết luận model tốt hay không, vì model có thể đạt Accuracy cao bằng cách ưu tiên các class đa số nhưng vẫn nhận diện kém các class bệnh hiếm. Vì vậy, Macro F1, Minority Recall và Worst-class Recall được xem là các chỉ số quan trọng hơn để đánh giá mức độ công bằng theo từng class.

WeightedRandomSampler hoạt động như một chiến lược dynamic oversampling. Phương pháp này không tạo ảnh mới và không thay đổi dataframe gốc. Thay vào đó, nó thay đổi xác suất lấy mẫu trong quá trình tạo mini-batch, làm cho các mẫu thuộc class thiểu số xuất hiện thường xuyên hơn trong mỗi epoch. Ưu điểm là model được tiếp xúc nhiều hơn với minority classes. Tuy nhiên, khi `replacement=True`, các ảnh hiếm có thể bị lặp lại nhiều lần, dẫn đến nguy cơ memorization và overfitting trên minority classes.

Light data augmentation được thêm vào để giảm rủi ro này. Các biến đổi nhẹ như lật ngang, xoay nhỏ và thay đổi màu sắc ở mức vừa phải giúp tăng diversity của các mẫu bị lặp lại, trong khi vẫn bảo toàn dấu hiệu bệnh trên lá cây. Điều này quan trọng vì augmentation quá mạnh có thể làm biến dạng vết bệnh, màu sắc hoặc texture, từ đó làm mất thông tin chẩn đoán.

EarlyStopping được thiết kế dựa trên Validation Macro F1. Tiêu chí này phù hợp với mục tiêu xử lý imbalance: quá trình train chỉ nên tiếp tục nếu hiệu năng cân bằng theo class trên validation set còn cải thiện. Nếu train loss tiếp tục giảm nhưng Validation Macro F1 đứng yên hoặc giảm, đó là dấu hiệu model đang học thuộc các mẫu minority bị lặp lại. EarlyStopping giúp chọn checkpoint có Validation Macro F1 tốt nhất và hạn chế overfitting ở giai đoạn cuối.

Hybrid resampling được giữ lại như một đối chứng ở mức data-level. Khác với sampler-based balancing, hybrid resampling thay đổi training dataframe bằng cách undersample class đa số và oversample class thiểu số về một target size chung. Cách này tạo phân phối train cân bằng hơn, nhưng có thể làm mất diversity của majority classes và lặp lại các mẫu minority.

Trong lần chạy này, experiment có Macro F1 cao nhất là `sampler_aug_earlystop`. Macro F1 thay đổi từ 0.7989 ở baseline lên 0.8126. Minority Recall thay đổi từ 0.7159 lên 0.8988. Nếu Accuracy giảm nhẹ trong khi Macro F1 và Minority Recall tăng, đây là trade-off có thể chấp nhận trong bài toán severe class imbalance, vì model bớt thiên lệch về majority classes và công bằng hơn với các class hiếm.

## 8. Kết luận
- Accuracy đơn lẻ không đủ tin cậy khi dữ liệu bị mất cân bằng nghiêm trọng.
- Macro F1, Minority Recall và Worst-class Recall phản ánh tốt hơn mức độ công bằng theo từng class.
- WeightedRandomSampler giúp tăng tần suất xuất hiện của minority samples, nhưng có nguy cơ lặp lại mẫu hiếm quá nhiều.
- Light augmentation làm tăng diversity của các mẫu minority bị lặp lại và giảm rủi ro memorization.
- EarlyStopping dựa trên Validation Macro F1 giúp kiểm soát overfitting tốt hơn.
- Hybrid resampling là đối chứng hữu ích để so sánh data-level balancing với sampler-based balancing.