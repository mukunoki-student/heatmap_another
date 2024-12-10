import os
from pathlib import Path
import re

# ファイルが保存されているディレクトリ
input_directory = Path("C:/Users/mukunoki/Desktop/heatmap_another/kawaguchi_images_png")

# ファイル名の変更
def rename_files(directory):
    # 1. ファイル名のリストを取得
    files = [f for f in directory.glob("*.png")]

    # 2. 数字部分を基準にソート（key引数を使用）
    sorted_files = sorted(files, key=lambda x: int(re.search(r'\d+', x.name).group()) if re.search(r'\d+', x.name) else float('inf'))

    # 3. ファイル名を新しい名前に変更
    new_index = 1  # 新しいインデックス（data01, data02, ...）
    for png_file in sorted_files:
        # 元のファイル名から数字部分を抽出
        match = re.search(r'図(\d+)', png_file.name)
        if match:
            original_number = int(match.group(1))

            # 図12をdata12に、図13以降をdata13に変換（連番のまま進む）
            if original_number >= 12:
                adjusted_index = original_number  # 図12はそのままdata12、以降はそのまま
            else:
                adjusted_index = original_number

            # XX は 2 桁の連番
            xx = f"{adjusted_index:02}"

            # Y は 1 か 2 (indexが11未満なら1、それ以外なら2)
            y = "1" if adjusted_index <= 11 else "2"

            # 新しいファイル名を作成
            new_file_name = f"data{xx}_shikuukann_{y}.png"
            new_file_path = input_directory / new_file_name

            # 4. ファイル名の変更
            os.rename(png_file, new_file_path)
            print(f"{png_file.name} -> {new_file_name}")

# 実行
rename_files(input_directory)



