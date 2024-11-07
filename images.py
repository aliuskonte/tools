def rotate_images(files_path, rotate='inverted'):
    """
    Поворачивает изображение и перезаписывает в ту же папку с тем же именем
    """
    left = cv2.ROTATE_90_COUNTERCLOCKWISE
    right = cv2.ROTATE_90_CLOCKWISE
    inverted = cv2.ROTATE_180
    
    if rotate == "left":
        rotate = left
    if rotate == "inverted":
        rotate = inverted
    if rotate == "right":
            rotate = right

    for im_name in list_files:
        image = cv2.imread(files_path / im_name)
        image = cv2.rotate(image, rotate)
        cv2.imwrite(files_path / im_name, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def convetr_to_jpg(files_path, folder_name="new_jpg_images"):
    """
    Конвертируем в джипег, удаляем старые расширения, добавляем .jpg
    """
    
    i = 0
    list_files = os.listdir(files_path)
    
    for image_name in list_files:
        image_name = Path(image_name)
        image = cv2.imread(files_path / image_name)

        # Удаляем разширение файла и сохраняем
        image_name_jpg = str(image_name.with_suffix(''))
        image_name_jpg = image_name_jpg + ".jpg"

        # Проверка на наличие папки для сохранения новых файлов
        Path(files_path / folder_name).mkdir(parents=True, exist_ok=True)

        # Сохраняем в новую папку
        cv2.imwrite(files_path / folder_name / image_name_jpg, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        i += 1
        
    print(f"Файлов сохранено: {i}")
    print("Done!")
