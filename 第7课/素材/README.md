# 第7课视觉素材

请把用于练习的图片放在本目录。为避免分发带版权或隐私风险的图片，仓库不内置真实照片。

推荐准备一张名为 `示例图.png` 的自制截图或图表；`例程/01_vision_base64.py` 未传路径时会默认读取它：

```powershell
python ..\例程\01_vision_base64.py
python ..\例程\01_vision_base64.py .\自己的图片.jpg --detail original
```

OpenCV 内存编码示例：

```powershell
# cv2.imread → cv2.imencode → Base64 data URL
python ..\例程\03_vision_opencv.py .\示例图.png --format jpg --transport base64

# cv2.imread → cv2.imencode → Files API；会保留远端文件并打印 file_id
python ..\例程\03_vision_opencv.py .\示例图.png --format png --transport files
```

不要把 `cv2.imread()` 返回的 NumPy 矩阵直接调用 `tobytes()` 后放入 JSON。裸像素缺少图片格式、尺寸和通道信息；必须先使用 `cv2.imencode()` 编码成 JPEG 或 PNG。OpenCV 的 BGR 矩阵可以直接交给 `imencode()`，无需先转换为 RGB。

素材要求：

- 格式：JPEG、PNG、GIF、WebP，以文件真实内容为准。
- Base64 单图不超过 32 MiB；请求体不超过 48 MiB。
- 图片最长边不超过 8192 像素；一次 15 张及以上时不超过 4096 像素。
- 不要使用含 API Key、身份证件、人脸、病历或其他敏感信息的图片。
- OCR 练习可用自制表格截图；图表练习可用自己生成的折线图或柱状图。
- JPEG 适合照片和摄像头帧；PNG 更适合文字、界面和图表。
- `--transport files` 会在账户中保留上传文件；请按第8课例程查询和删除不再使用的文件。
