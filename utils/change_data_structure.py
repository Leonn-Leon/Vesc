import os
import shutil

# Путь к исходной папке датасета
source_dataset = '/storage/vskovoroda/Grape/human_and_hands/hand_dataset'

# Пути для новой структуры
target_images = os.path.join(source_dataset, 'images')
target_labels = os.path.join(source_dataset, 'labels')

# Создаем основные папки images и labels, если они еще не созданы
os.makedirs(target_images, exist_ok=True)
os.makedirs(target_labels, exist_ok=True)

# Словарь для маппинга старых папок в новые
data_types = {'training_dataset/training_data': 'train',
              'validation_dataset/validation_data': 'validation',
              'test_dataset/test_data': 'test'}

# Перебираем каждый тип данных (train, validation, test)
for old_folder, new_folder in data_types.items():
    # Создаем новые папки для images и labels
    new_image_path = os.path.join(target_images, new_folder)
    new_label_path = os.path.join(target_labels, new_folder)
    os.makedirs(new_image_path, exist_ok=True)
    os.makedirs(new_label_path, exist_ok=True)

    # Копирование и переименование изображений
    old_image_path = os.path.join(source_dataset, old_folder, 'images')
    old_label_path = os.path.join(source_dataset, old_folder,
                                  'new_annotations')  # Предполагаем, что new_annotations содержат нужные аннотации

    # Копируем файлы изображений
    for image_file in os.listdir(old_image_path):
        shutil.copy(os.path.join(old_image_path, image_file), os.path.join(new_image_path, image_file))

    # Копируем аннотации
    for label_file in os.listdir(old_label_path):
        shutil.copy(os.path.join(old_label_path, label_file), os.path.join(new_label_path, label_file))

print("Данные успешно переорганизованы.")
