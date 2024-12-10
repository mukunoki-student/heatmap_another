import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd

df = pd.read_csv("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv/202202226-006_csv/data01_shikuukann_1.csv")

df = df.dropna(axis=0)  # NaN を含む列を削除


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

    if imgfile.any():
        h, w, _ = imgfile.shape
        heatmap = cv2.resize(heatmap, (w, h))
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)



        mask = np.where(heatmap <= threshold, 1, 0).reshape(h, w, 1)
        mask = np.repeat(mask, 3, axis=2)

        marge = imgfile * mask + heatmap_color * (1 - mask)
        marge = cv2.addWeighted(imgfile, 1 - alpha, marge.astype("uint8"), alpha, 0)
        return marge
    else:
        return cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

if __name__ == '__main__':
    img = cv2.imread("C:/Users/mukunoki/Desktop/heatmap_another/example.png")
    H, W, _ = img.shape

    fix_arr = df[['GazePointX', 'GazePointY']].values
    fix_arr -= fix_arr.min()
    fix_arr /= fix_arr.max()
    fix_arr[:, 0] *= W
    fix_arr[:, 1] *= H
    #fix_arr[:, 1] = H - fix_arr[:, 1]  # x座標を反転
    #fix_arr = fix_arr[:, [1, 0]]  # これにより x と y を入れ替える

heatmap = Fixpos2Densemap(fix_arr, W, H, img, 0.7, 5)
cv2.imwrite("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv_heatmap_another/output1.png", heatmap)

if img is None:
    print("画像が読み込めませんでした")
else:
    print("画像のサイズ:", img.shape)
