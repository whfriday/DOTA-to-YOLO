def convert_to_yolo_format(coordinates, class_index, image_width, image_height):
    """Алгоритм пересчёта из формата DOTA в YOLO"""

    x1, y1, x2, y2, x3, y3, x4, y4 = coordinates

    min_x = min(x1, x2, x3, x4)
    max_x = max(x1, x2, x3, x4)
    min_y = min(y1, y2, y3, y4)
    max_y = max(y1, y2, y3, y4)

    x_center = (min_x + max_x) / 2.0
    y_center = (min_y + max_y) / 2.0
    width_box = max_x - min_x
    height_box = max_y - min_y

    x_center_norm = x_center / image_width
    y_center_norm = y_center / image_height
    width_norm = width_box / image_width
    height_norm = height_box / image_height

    return f"{class_index} {x_center_norm} {y_center_norm} {width_norm} {height_norm}"


def process_file(input_file, output_file, image_width, image_height):
    """Перезапись пересчитанных данных в новый файл"""

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()[2:]  #чтение файла со второй строки(особенность DOTA)

        for line in lines:
            parts = line.strip().split()
            valid_classes = ['0', '1']  #необходимые индексы класса объектов
            class_index_old = parts[8]
            if class_index_old == 'plane':
                class_index = '0'
            elif class_index_old == 'helicopter':
                class_index = '1'
            else:
                class_index = None
            
            #данные, в которых не присутствует объект необходимого класса - не записываются в новый файл
            if class_index in valid_classes:
                coordinates = list(map(float, parts[0:8]))
                yolo_format_line = convert_to_yolo_format(
                    coordinates, class_index, image_width, image_height
                )
                outfile.write(yolo_format_line + "\n")
            else:
                continue


# Параметры
input_file = r"<путь к фалу в формате DOTA>"
output_file = r"<путь к файлу в формате YOLO>"
image_width = 2832  #длина изображения(в пикселях)
image_height = 3205     #высота изображения(в пикселях)

# Обработка файла
process_file(input_file, output_file, image_width, image_height)
