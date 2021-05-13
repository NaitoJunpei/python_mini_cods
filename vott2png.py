#coding: utf-8

"""
アノテーション用ソフト Vottで囲んだ部分を白とする画像を生成する
(複数タグには対応していない　今後対応する必要もあるかも)
"""

import sys
from PIL import Image, ImageDraw
import json
import os

def vott2png(import_filename, export_foldername) :
    f = open(import_filename)
    json_file = json.load(f)
    f.close()
    names = []
    flag = False

    for data in json_file["assets"] :
        data = json_file["assets"][data]
        height = data["asset"]["size"]["height"]
        width = data["asset"]["size"]["width"]
        img = Image.new('L', (height, width), 0)

        for data_i in data["regions"] :
            flag = False
            if data_i["type"] != "POLYGON" :
                continue
            flag = True
            name = "t_" + data["asset"]["name"]
            l = list(map(lambda point : (int(point["x"]), int(point["y"])), data_i["points"]))
            ImageDraw.Draw(img).polygon(l, outline=255, fill=255)
        if(flag) :
            img.save(export_foldername + name[:-4] + ".png")

def main() :
    args = sys.argv
    if len(args) < 3 :
        print("ファイル名、フォルダ名の入力が必要です")
        print("python vott2png.py <ファイル名> <フォルダ名>")
        exit()

    filename = args[1]
    foldername = args[2]
    if not(os.path.isfile(filename)) or not(os.path.isdir(foldername)) :
        print("ファイル、又はフォルダが存在しません")
        exit()

    vott2png(filename, foldername)

if __name__ == "__main__" :
    main()
