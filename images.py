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
