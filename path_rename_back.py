import os
from pathlib import Path

# ファイルが保存されているディレクトリ
input_directory = Path("C:/Users/mukunoki/Desktop/heatmap_another/kawaguch_images_png")

# ファイル名を元に戻す関数
def restore_files(directory):
    # 元の名前が記録されたファイルを読み込む
    with open('original_names.txt', 'r') as f:
        # ファイル名の変更履歴をリストに格納
        rename_history = [line.strip().split(' -> ') for line in f.readlines()]

    # 変更履歴を基にファイル名を戻す
    for original_name, new_name in rename_history:
        # 元のファイルと新しいファイルのパスを作成
        original_file_path = directory / new_name
        restored_file_path = directory / original_name
        
        # ファイル名を元に戻す
        if original_file_path.exists():
            os.rename(original_file_path, restored_file_path)
            print(f"{new_name} -> {original_name} に戻しました。")
        else:
            print(f"{new_name} は存在しないため戻せません。")

# 実行
restore_files(input_directory)
