import random
import json
from PIL import Image, ImageDraw
import os


def get_file_names_in_folder(folder_path):
    file_names = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_names.append(filename)
    return file_names


# 替换为您的文件夹路径
object_path = "../object/"
background_path = "../background/"
output_folder_path = "../DataOut/"

# 获取待选图片列表
candidate_images = get_file_names_in_folder(object_path)

# 生成图像的数量
num_images = 100

# 生成图像的尺寸
image_width = 1000
image_height = 1000

# 固定object图片的尺寸
object_width = 100
object_height = 100

# 创建输出文件夹
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 生成图像并保存
for i in range(num_images):
    background = Image.open(background_path + "background.png").resize((image_width, image_height))
    draw = ImageDraw.Draw(background)

    selected_candidates = random.sample(candidate_images, 10)
    image_data = []

    for candidate in selected_candidates:
        x = random.randint(0, image_width - object_width)
        y = random.randint(0, image_height - object_height)
        candidate_image = Image.open(os.path.join(object_path, candidate)).resize((object_width, object_height))
        background.paste(candidate_image, (x, y))

        # 计算归一化坐标并保留小数点后5位
        x_normalized = round(x / image_width, 5)
        y_normalized = round(y / image_height, 5)
        width_normalized = round(object_width / image_width, 5)
        height_normalized = round(object_height / image_height, 5)

        image_data.append({"class": candidate, "x_center": round(x_normalized + width_normalized / 2, 5),
                           "y_center": round(y_normalized + height_normalized / 2, 5), "width": width_normalized,
                           "height": height_normalized})

    background.save(os.path.join(output_folder_path, f"image_{i}.jpg"))

    json_data = {"image": f"image_{i}.jpg", "candidates": image_data}
    with open(os.path.join(output_folder_path, f"image_{i}.json"), "w") as json_file:
        json.dump(json_data, json_file, indent=4)
