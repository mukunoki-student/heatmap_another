import os
from PIL import Image

# 変換対象のディレクトリを指定
input_directory = "C:/Users/mukunoki/Desktop/heatmap_another/kawaguch_images"
output_directory = "C:/Users/mukunoki/Desktop/heatmap_another/kawaguchi_images_png"

# 出力フォルダが存在しない場合は作成
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# ディレクトリ内のすべてのJPGファイルをPNGに変換
for filename in os.listdir(input_directory):
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        img_path = os.path.join(input_directory, filename)
        img = Image.open(img_path)
        
        # 拡張子をPNGに変更して保存
        png_filename = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(output_directory, png_filename)
        img.save(output_path, "PNG")
        print(f"変換: {filename} -> {png_filename}")

print("すべてのJPGファイルがPNGに変換されました！")
