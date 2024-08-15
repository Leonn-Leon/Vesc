import os
import shutil

# Определение пути к основной папке датасета
base_path = 'egohands'

# Пути к исходным и целевым папкам для изображений и аннотаций
image_folders = {
    'train': os.path.join(base_path, 'images', 'train'),
    'test': os.path.join(base_path, 'images', 'test')
}
label_folders = {
    'train': os.path.join(base_path, 'labels', 'train'),
    'test': os.path.join(base_path, 'labels', 'test')
}

# Создание целевых папок для аннотаций, если они еще не существуют
for label_folder in label_folders.values():
    os.makedirs(label_folder, exist_ok=True)

# Перемещение аннотаций из папок с изображениями в новые папки с аннотациями
for data_type in image_folders:
    current_image_folder = image_folders[data_type]
    current_label_folder = label_folders[data_type]

    # Обход файлов в папке с изображениями
    for filename in os.listdir(current_image_folder):
        # Определение пути к текущему файлу
        file_path = os.path.join(current_image_folder, filename)

        # Проверка, является ли файл аннотацией (например, файлы .txt)
        if filename.endswith('.txt'):
            # Определение нового пути для файла аннотации
            new_file_path = os.path.join(current_label_folder, filename)
            # Перемещение файла аннотации
            shutil.move(file_path, new_file_path)
            print(f'Moved {file_path} to {new_file_path}')

print("Структура датасета успешно обновлена.")
