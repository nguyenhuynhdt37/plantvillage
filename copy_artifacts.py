import shutil
from pathlib import Path

src_dir = Path('/Users/huynh/codes/kpdl/plan/results')
dst_dir = Path('/Users/huynh/.gemini/antigravity/brain/018d8519-b81e-4e00-8820-93c5beed240f')

dst_dir.mkdir(parents=True, exist_ok=True)

shutil.copy(src_dir / 'class_distribution_chart.png', dst_dir / 'class_distribution_chart.png')
shutil.copy(src_dir / 'confusion_matrix_comparison.png', dst_dir / 'confusion_matrix_comparison.png')
shutil.copy(src_dir / 'gradcam_visualizations/correct_minority_gradcam.png', dst_dir / 'correct_minority_gradcam.png')
shutil.copy(src_dir / 'gradcam_visualizations/diff_prediction_gradcam.png', dst_dir / 'diff_prediction_gradcam.png')

print("All artifact images copied successfully!")
