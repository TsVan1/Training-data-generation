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

# 待选图片的尺寸
candidate_width = 100
candidate_height = 100

# 创建输出文件夹
if not os.path.exists("output"):
    os.makedirs("output")

# 生成图像并保存
for i in range(num_images):
    background = Image.open(background_path+"background.png").resize((image_width, image_height))
    draw = ImageDraw.Draw(background)

    selected_candidates = random.sample(candidate_images, 10)
    image_data = []

    for candidate in selected_candidates:
        x = random.randint(0, image_width - candidate_width)
        y = random.randint(0, image_height - candidate_height)
        candidate_image = Image.open(os.path.join(object_path, candidate)).resize((candidate_width, candidate_height))
        background.paste(candidate_image, (x, y))
        image_data.append({"name": candidate, "x": x, "y": y})

    background.save(f"../DataOut/image_{i}.jpg")

    json_data = {"image": f"image_{i}.jpg", "candidates": image_data}
    with open(os.path.join(output_folder_path , f"image_{i}.json"), "w") as json_file:
        json.dump(json_data, json_file, indent=4)