import pandas as pd
import cv2
import json

import rupasportread as pr


def to_correct_coordinates(df, i):

    """Преобразуем координаты для выделенных частей изображения в пиксели
    Args:
        df: данные из csv
        i: int - номер строки
    :returns
        new_labels: список с новыми координатами
    """

    ser_label = df['label']
    labels = json.loads(ser_label[i])
    new_labels = []

    for label in labels:
        x_center = label['x']
        y_center = label['y']
        width_box = label['width']
        height_box = label['height']
        image_width = label['original_width']
        image_height = label['original_height']
        x = int(round((x_center * image_width) / 100, 0))
        y = int(round((y_center * image_height) / 100, 0))
        w = int(round((width_box * image_width) / 100, 0))
        h = int(round((height_box * image_height) / 100, 0))
        new_l = [x, y, w, h]
        new_labels.append(new_l)
    return new_labels


def to_make_csv(path_csv):

    """
    Создаем новую таблицу с координатами для выделенных частей изображения,
    названием фрагмента и названием файла

    Args:
        path_csv: путь к csv-файлу
    Returns:
        df_pass: таблица с координатами для выделенных частей изображения
    """

    df = pd.read_csv(path_csv)
    df_pass = pd.DataFrame(columns=['x', 'y', 'width', 'height', 'transcription', 'name'])

    for i in range(len(df)):
        new_labels = to_correct_coordinates(df, i)
        df_new = pd.DataFrame(new_labels)
        df_new.rename(columns={0: "x", 1: "y", 2: "width", 3: "height"}, inplace=True)
        ser_transcription = df['transcription']
        transcriptions = json.loads(ser_transcription[i])
        df_new.loc[:, "transcription"] = transcriptions
        name = df['ocr'][i]
        name = name.rsplit('/')[-1]
        name = name.rsplit('-')[1:]
        name = "-".join(name)
        df_new.loc[:, "name"] = name
        df_pass = pd.concat([df_pass, df_new], ignore_index=True)
    numbers = list(range(0, len(df_pass)))

    return df_pass, numbers


def main(df_pass, path_read_img, path_save_img):

    """
    Сохраняем выделенные части изображения
    """

    for i in range(len(df_pass)):
        x = df_pass['x'][i]
        y = df_pass['y'][i]
        w = df_pass['width'][i]
        h = df_pass['height'][i]
        img_name = df_pass['name'][i]
        image = cv2.imread(path_read_img + "/" + img_name)
        cropp_image = image[y:y + h, x:x + w]
        df_pass["name"][i] = str(i) + "-" + img_name
        cv2.imwrite(path_save_img + "/" + str(i) + "-" + img_name, cropp_image)
      

#js = pr.catching('data/first_pass_page_I/I/0BA06FA4-180D-489F-9D43-76BD8A74071F_first_pass_page.JPG')

#df_passports, _ = to_make_csv("csv/project-1-at-2024-10-26-14-37-92cb01a1.csv")
#main(df_passports, path_read_img="data/first_pass_page_I/I", path_save_img="cutting")

#df_passports.to_csv("csv/data.csv", index=False)
#print(df_passports)
