import cv2
import numpy as np
from scipy.fft import fft

from hb_core.dtos.dto import CalculateParameterReturnValue
from hb_core.error.error_code import ErrorCode
from hb_core.repositories.system import exists_path, read_binary


def calculate_artistry(file_content: bytes) -> CalculateParameterReturnValue:
    # 画像の読み込み
    # バイナリデータを numpy.ndarray に変換（画像をロード）
    np_image = np.frombuffer(file_content, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # 画像をグレースケールに変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二値化処理を行い、輪郭を検出するためのマスクを作成
    _, binary_image = cv2.threshold(gray_image, 100, 200, cv2.THRESH_BINARY)

    # 輪郭検出
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # 輪郭の中心を計算
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0

    # 輪郭上の各点から重心までの距離を計算
    distances = []
    for point in largest_contour:
        x, y = point[0]
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        distances.append(distance)

    # フーリエ変換
    signal = np.array(distances)
    fourier_transform = fft(signal)

    # フーリエ変換の結果を使用して寝癖を数値化
    magnitude_spectrum = np.abs(fourier_transform)
    sleep_magnitude = magnitude_spectrum[1]  # 高周波成分を取得

    # 寝癖の数値を返す
    return CalculateParameterReturnValue(
        error_codes=(),
        parameter=sleep_magnitude,
    )


def get_artistry(file_path: str) -> CalculateParameterReturnValue:
    if not exists_path(file_path):
        return CalculateParameterReturnValue(
            error_codes=(ErrorCode.FILE_NOT_EXIST,),
            parameter=0,
        )

    # ファイルが JPEG 形式かどうかを確認
    if file_path.lower().endswith(".jpg"):
        return calculate_artistry(read_binary(file_path))
    else:
        return CalculateParameterReturnValue(
            error_codes=(ErrorCode.FILE_NOT_EXIST,),
            parameter=0,
        )
