import os

import cv2
import numpy as np
from ultralytics import YOLO

from hb_core.dtos.dto import CalculateParameterReturnValue
from hb_core.error.error_code import ErrorCode


def calculate_explosiveness(file_path: str) -> CalculateParameterReturnValue:
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    # 画像を読み込む
    frame = cv2.imread(file_path)

    # YOLO モデルの初期化
    model = YOLO("models/best.pt")

    # 画像から物体検出を実行
    results = model(frame)
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")

    # classes が 0 および 1 の矩形の面積を計算
    area_class_0 = 0
    area_class_1 = 0
    class_0_count = 0
    class_1_count = 0

    for i in range(len(bboxes)):
        if classes[i] == 0:
            area_class_0 += (bboxes[i][2] - bboxes[i][0]) * (
                bboxes[i][3] - bboxes[i][1]
            )
            class_0_count += 1
        elif classes[i] == 1:
            area_class_1 += (bboxes[i][2] - bboxes[i][0]) * (
                bboxes[i][3] - bboxes[i][1]
            )
            class_1_count += 1

    # classes が 0 または 1 の矩形が1つずつ検出された場合、面積の比を計算
    if class_0_count == 1 and class_1_count == 1:
        explosiveness_ratio = area_class_0 / area_class_1
        return CalculateParameterReturnValue(
            error_codes=(), parameter=explosiveness_ratio
        )
    else:
        return CalculateParameterReturnValue(
            error_codes=(ErrorCode.NO_VALID_OBJECT_CLASS_DETECTED,), parameter=0
        )

    # 検出された物体のバウンディングボックス情報を表示
    # for cls, bbox in zip(classes, bboxes):
    #     (x, y, x2, y2) = bbox
    #     print("class", str(cls), "x", x, "y", y, "x2", x2, "y2", y2)
    # cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
    # cv2.putText(frame, str(cls), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)

    # 画像を表示
    # cv2.imshow("Img", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
