import random
from PIL import Image, ImageDraw, ImageOps
import os

# 配置参数
object_path = "../object/"
background_path = "../background/"
output_folder_path = "../DataOut/"
num_images = 100
image_size = (1024, 1024)
object_size = (100, 100)
border_width = 5

# 检查输出文件夹是否存在，不存在则创建
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 获取待选图片列表
def get_file_names_in_folder(folder_path):
    file_names = {}
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_name_without_extension = os.path.splitext(filename)[0]
            file_names[file_name_without_extension] = filename
    return file_names

candidate_images = get_file_names_in_folder(object_path)

# 创建文件名到数字的映射字典
file_name_to_number_mapping = {name: i for i, name in enumerate(candidate_images)}

# 函数：将对象裁剪为圆形
def crop_to_circle(image):
    circle_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)
    circle_image.paste(image, mask=mask)
    return circle_image

# 函数：在对象位置绘制圆形边框
def draw_circular_border(image, border_color):
    border_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(border_image)
    center_x, center_y = image.size[0] // 2, image.size[1] // 2
    radius = image.size[0] // 2
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline=border_color, width=border_width)
    result = Image.alpha_composite(image.convert("RGBA"), border_image)
    return result

# 生成图像并保存
for i in range(num_images):
    background = Image.open(background_path + "background.png").resize(image_size)
    draw = ImageDraw.Draw(background)
    selected_candidates = random.sample(list(candidate_images.keys()), 10)
    txt_data = []

    for candidate in selected_candidates:
        center_x = random.randint(object_size[0] // 2, image_size[0] - object_size[0] // 2)
        center_y = random.randint(object_size[1] // 2, image_size[1] - object_size[1] // 2)
        x, y = center_x - object_size[0] // 2, center_y - object_size[1] // 2

        candidate_image = Image.open(os.path.join(object_path, candidate_images[candidate])).convert("RGBA")
        candidate_image = crop_to_circle(candidate_image)

        border_color = (random.randint(0, 255), 0, 0, 255) if random.random() < 0.5 else (0, 0, random.randint(0, 255), 255)
        candidate_image = draw_circular_border(candidate_image, border_color)
        candidate_image = candidate_image.resize(object_size)

        background.paste(candidate_image, (x, y), candidate_image)

        x_normalized = round(center_x / image_size[0], 5)
        y_normalized = round(center_y / image_size[1], 5)
        width_normalized = round(object_size[0] / image_size[0], 5)
        height_normalized = round(object_size[1] / image_size[1], 5)

        class_number = file_name_to_number_mapping[candidate]
        txt_data.append(
            f"{class_number} {x_normalized:.5f} {y_normalized:.5f} {width_normalized:.5f} {height_normalized:.5f}")

    background.save(os.path.join(output_folder_path, f"image_{i}.jpg"))

    with open(os.path.join(output_folder_path, f"image_{i}.txt"), "w") as txt_file:
        txt_file.write("\n".join(txt_data))

# 生成类别名称到数字的映射关系txt文件
with open(os.path.join(output_folder_path, "class_mapping.txt"), "w") as mapping_file:
    for name, number in file_name_to_number_mapping.items():
        mapping_file.write(f"{number}: {name}\n")
