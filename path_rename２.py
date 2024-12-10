import os
from pathlib import Path
import re

# ファイルが保存されているディレクトリ
input_directory = Path("C:/Users/mukunoki/Desktop/heatmap_another/kawaguch_images_png")

# ファイル名の変更
def rename_files(directory):
    # 1. ファイル名のリストを取得
    #fはfilesのこと
    files = [f for f in directory.glob("*.png")]

    # 2. 数字部分を基準にソート（key引数を使用）
    #r'\d+'→1桁以上の数字を見つけるもの
    sorted_files = sorted(files, key=lambda x: int(re.search(r'\d+', x.name).group()))

    # 3. 元の名前をリストに保存
    original_names = [(file.name, file) for file in sorted_files]


    # 3. ファイル名を新しい名前に変更
    for index, png_file in enumerate(sorted_files, start=1):
        # XX は 2 桁の連番
        xx = f"{index:02}"
        
        # Y は 1 か 2
        y = "1" if index <= 11 else "2"
        
        # 新しいファイル名を作成
        new_file_name = f"data{xx}_shikuukann_{y}.png"
        new_file_path = input_directory / new_file_name

        # 4. ファイル名の変更
        os.rename(png_file, new_file_path)
        print(f"{png_file.name} -> {new_file_name}")

    with open('original_names.txt', 'w') as f:
        for original_name, file in original_names:
            f.write(f"{original_name} -> {file.name}\n")

# 実行
rename_files(input_directory)
