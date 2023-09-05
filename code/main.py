import random
from PIL import Image, ImageDraw
import os


def get_file_names_in_folder(folder_path):
    file_names = {}
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_name_without_extension = os.path.splitext(filename)[0]
            file_names[file_name_without_extension] = filename
    return file_names


# 替换为您的文件夹路径
object_path = "../object/"
background_path = "../background/"
output_folder_path = "../DataOut/"

# 获取待选图片列表，使用字典映射文件名到图片名称去掉后缀
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

# 生成文件名到数字的映射字典
file_name_to_number_mapping = {name: i for i, name in enumerate(candidate_images)}

# 生成图像并保存
for i in range(num_images):
    background = Image.open(background_path + "background.png").resize((image_width, image_height))
    draw = ImageDraw.Draw(background)

    selected_candidates = random.sample(list(candidate_images.keys()), 10)

    txt_data = []

    for candidate in selected_candidates:
        # 计算object中心点坐标
        center_x = random.randint(object_width // 2, image_width - object_width // 2)
        center_y = random.randint(object_height // 2, image_height - object_height // 2)

        # 计算左上角坐标
        x = center_x - object_width // 2
        y = center_y - object_height // 2

        candidate_image = Image.open(os.path.join(object_path, candidate_images[candidate])).resize(
            (object_width, object_height))
        background.paste(candidate_image, (x, y))

        # 计算归一化坐标并保留小数点后5位
        x_normalized = round(center_x / image_width, 5)
        y_normalized = round(center_y / image_height, 5)
        width_normalized = round(object_width / image_width, 5)
        height_normalized = round(object_height / image_height, 5)

        class_number = file_name_to_number_mapping[candidate]  # 使用数字作为类别
        txt_data.append(
            f"{class_number} {x_normalized:.5f} {y_normalized:.5f} {width_normalized:.5f} {height_normalized:.5f}")

    background.save(os.path.join(output_folder_path, f"image_{i}.jpg"))

    with open(os.path.join(output_folder_path, f"image_{i}.txt"), "w") as txt_file:
        txt_file.write("\n".join(txt_data))

# 生成类别名称到数字的映射关系txt文件
with open(os.path.join(output_folder_path, "class_mapping.txt"), "w") as mapping_file:
    for name, number in file_name_to_number_mapping.items():
        mapping_file.write(f"{number} {name}\n")
