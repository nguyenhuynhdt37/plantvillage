import shutil
from pathlib import Path

project_dir = Path(__file__).resolve().parent
src_dir = project_dir / 'results'
dst_dir = project_dir / 'reports' / 'copied_artifacts'

dst_dir.mkdir(parents=True, exist_ok=True)

shutil.copy(src_dir / 'class_distribution_chart.png', dst_dir / 'class_distribution_chart.png')
shutil.copy(src_dir / 'confusion_matrix_comparison.png', dst_dir / 'confusion_matrix_comparison.png')
shutil.copy(src_dir / 'gradcam_visualizations/correct_minority_gradcam.png', dst_dir / 'correct_minority_gradcam.png')
shutil.copy(src_dir / 'gradcam_visualizations/diff_prediction_gradcam.png', dst_dir / 'diff_prediction_gradcam.png')

print("All artifact images copied successfully!")
