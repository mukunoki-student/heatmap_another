import cv2
import numpy as np
#tqdm使いやすいからよし
from tqdm import tqdm
import pandas as pd
from pathlib import Path

# 入力フォルダのパス
csv_base_path = Path("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv")
image_base_path = Path("C:/Users/mukunoki/Desktop/heatmap_another/kawaguchi_images_png")
output_base_path = Path("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv_heatmap_another")

# 各被験者フォルダごとに処理
for csv_subject_folder in csv_base_path.glob("*"):
    if not csv_subject_folder.is_dir():
        continue

    subject_name = csv_subject_folder.name
    output_subject_folder = output_base_path / subject_name 
    output_subject_folder.mkdir(parents=True, exist_ok=True)

    # CSVファイルごとに処理
    for csv_file in csv_subject_folder.glob("*.csv"):
        # CSVファイルの読み込み
        df = pd.read_csv(csv_file)
        df = df.dropna(axis=0)  # NaNを含む行を削除

        def GaussianMask(sizex, sizey, sigma=33, center=None, fix=1):
            x = np.arange(0, sizex, 1, float)
            y = np.arange(0, sizey, 1, float)
            x, y = np.meshgrid(x, y)

            if center is None:
                x0 = sizex // 2
                y0 = sizey // 2
            else:
                if not np.isnan(center[0]) and not np.isnan(center[1]):
                    x0 = center[0]
                    y0 = center[1]
                else:
                    return np.zeros((sizey, sizex))

            return fix * np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / sigma ** 2)

        def Fixpos2Densemap(fix_arr, width, height, imgfile, alpha=0.5, threshold=10):
            heatmap = np.zeros((height, width), np.float64)
            for n_subject in tqdm(range(fix_arr.shape[0])):
                heatmap += GaussianMask(width, height, 33, (fix_arr[n_subject, 0], fix_arr[n_subject, 1]))

            # 正規化して 0-255 の範囲にスケーリング
            heatmap = heatmap / np.amax(heatmap)
            heatmap = (heatmap * 255).astype("uint8")

            if imgfile is not None and imgfile.size > 0:
                h, w, _ = imgfile.shape
                heatmap = cv2.resize(heatmap, (w, h))
                heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

                mask = np.where(heatmap <= threshold, 1, 0).reshape(h, w, 1)
                mask = np.repeat(mask, 3, axis=2)

                merged = imgfile * mask + heatmap_color * (1 - mask)
                merged = cv2.addWeighted(imgfile, 1 - alpha, merged.astype("uint8"), alpha, 0)
                return merged
            else:
                return cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # 対応するPNG画像を検索
        #stem→ファイル名から拡張子を取り除いたものを指す
        corresponding_png = image_base_path /f"{csv_file.stem}.png"
        if not corresponding_png.exists():
            print(f"画像 {corresponding_png} が見つかりませんでした")
            continue

        # 画像の読み込み
        img = cv2.imread(str(corresponding_png))
        if img is None:
            print(f"画像 {corresponding_png} が読み込めませんでした")
            continue

        H, W, _ = img.shape

        # GazePointX, GazePointY の正規化とスケーリング
        fix_arr = df[['GazePointX', 'GazePointY']].values
        #fix_arr -= fix_arr.min(axis=0)
        #fix_arr /= fix_arr.max(axis=0)
        #fix_arr[:, 0] *= W
        #fix_arr[:, 1] *= H

        # ヒートマップの生成と重ね合わせ
        heatmap = Fixpos2Densemap(fix_arr, W, H, img, alpha=0.7, threshold=5)
        output_file_path = output_subject_folder / f"{csv_file.stem}_heatmap.png"
        cv2.imwrite(str(output_file_path), heatmap)

        print(f"ヒートマップを {output_file_path} に保存しました")
               
