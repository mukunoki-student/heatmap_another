import os
from pathlib import Path

# フォルダのパスを指定
folder_path = Path("C:/Users/mukunoki/Desktop/heatmap_another/heatmap_image_png")  # 変更が必要

# フォルダ内のすべての PNG ファイルを取得
#globで探索し、sortedで並べてる
png_files = sorted(folder_path.glob("図*.png"))

# ファイルの名前を変更
for index, png_file in enumerate(png_files, start=1):
    # XX は 2 桁の連番
    xx = f"{index:02}"
    
    # Y は 1 か 2
    y = "1" if index <= 11 else "2"
    
    # 新しいファイル名を作成
    new_file_name = f"data{xx}_shikuukann_{y}.png"
    new_file_path = folder_path / new_file_name

    # ファイルの名前を変更
    png_file.rename(new_file_path)

    print(f"{png_file.name} を {new_file_name} に変更しました")
