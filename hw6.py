import pathlib
import sys
import os
import shutil
from random import randint


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "e", "u", "ja")

TRANS = {}

for cs, trl in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cs)] = trl
    TRANS[ord(cs.upper())] = trl.upper()


def normalize(name: str) -> str:
    trl_name = name.translate(TRANS)
    trl_name = re.sub(r"\W", "_", trl_name)
    return trl_name

def filterDir(path):

    png = [x for x in os.listdir(path) if x.count(".png") or x.count(".PNG")]
    jpeg = [x for x in os.listdir(path) if x.count("jpeg") or x.count(".JPEG")]
    jpg = [x for x in os.listdir(path) if x.count(".jpg") or x.count(".JPG")]
    svg = [x for x in os.listdir(path) if x.count(".svg") or x.count(".SVG")]
    if len(png)|len(jpeg)|len(jpg)|len(svg)>0:
        os.mkdir(f"{path}/images")
        for el in png:
            os.rename(f"{path}/{el}", f"{path}/images/{normalize(el[:-4])}{'.png'}")
        for el in jpeg:
            os.rename(f"{path}/{el}", f"{path}/images/{normalize(el[:-5])}{'.jpeg'}")
        for el in jpg:
            os.rename(f"{path}/{el}", f"{path}/images/{normalize(el[:-4])}{'.jpg'}")
        for el in svg:
            os.rename(f"{path}/{el}", f"{path}/images/{normalize(el[:-4])}{'.svg'}")

    avi = [x for x in os.listdir(path) if x.count(".avi") or x.count(".AVI")]
    mp4 = [x for x in os.listdir(path) if x.count(".mp4") or x.count(".MP4")]
    mov = [x for x in os.listdir(path) if x.count(".mov") or x.count(".MOV")]
    mkv = [x for x in os.listdir(path) if x.count(".mkv") or x.count(".MKV")]
    if len(avi) | len(mp4) | len(mov) | len(mkv) > 0:
        os.mkdir(f"{path}/video")
        for el in avi:
            os.rename(f"{path}/{el}", f"{path}/video/{normalize(el[:-4])}{'.avi'}")
        for el in mp4:
            os.rename(f"{path}/{el}", f"{path}/video/{normalize(el[:-4])}{'.mp4'}")
        for el in mov:
            os.rename(f"{path}/{el}", f"{path}/video/{normalize(el[:-4])}{'.mov'}")
        for el in mkv:
            os.rename(f"{path}/{el}", f"{path}/video/{normalize(el[:-4])}{'.mkv'}")

    docx = [x for x in os.listdir(path) if x.count(".doc") or x.count(".DOC")]
    txt = [x for x in os.listdir(path) if x.count(".txt") or x.count(".TXT")]
    pdf = [x for x in os.listdir(path) if x.count(".pdf") or x.count(".PDF")]
    xlsx = [x for x in os.listdir(path) if x.count(".xlsx") or x.count(".XLSX")]
    pptx = [x for x in os.listdir(path) if x.count(".pptx") or x.count(".PPTX")]
    if  len(txt) | len(pdf) | len(xlsx) | len(pptx)> 0:
        os.mkdir(f"{path}/documents")
        for el in docx:
            os.rename(f"{path}/{el}", f"{path}/documents/{normalize(el[:-5])}{el[-5:]}")
        for el in txt:
            os.rename(f"{path}/{el}", f"{path}/documents/{normalize(el[:-4])}{'.txt'}")
        for el in pdf:
            os.rename(f"{path}/{el}", f"{path}/documents/{normalize(el[:-4])}{'.pdf'}")
        for el in xlsx:
            os.rename(f"{path}/{el}", f"{path}/documents/{normalize(el[:-5])}{'.xlsx'}")
        for el in pptx:
            os.rename(f"{path}/{el}", f"{path}/documents/{normalize(el[:-5])}{'.pptx'}")

    mp3 = [x for x in os.listdir(path) if x.count(".mp3") or x.count(".MP3")]
    ogg = [x for x in os.listdir(path) if x.count(".ogg") or x.count(".OGG")]
    wav = [x for x in os.listdir(path) if x.count(".wav") or x.count(".WAV")]
    amr = [x for x in os.listdir(path) if x.count(".amr") or x.count(".AMR")]
    if len(mp3) | len(ogg) | len(wav) | len(amr) > 0:
        os.mkdir(f"{path}/audio")
        for el in mp3:
            os.rename(f"{path}/{el}", f"{path}/audio/{el}")
        for el in ogg:
            os.rename(f"{path}/{el}", f"{path}/audio/{el}")
        for el in wav:
            os.rename(f"{path}/{el}", f"{path}/audio/{el}")
        for el in amr:
            os.rename(f"{path}/{el}", f"{path}/audio/{el}")

    zip = [x for x in os.listdir(path) if x.count(".zip") or x.count(".ZIP")]
    gz = [x for x in os.listdir(path) if x.count(".gz") or x.count(".GZ")]
    tar = [x for x in os.listdir(path) if x.count(".tar") or x.count(".TAR")]
    if len(zip) | len(gz) | len(tar) > 0:
        os.mkdir(f"{path}/archives")
        for el in zip:
            os.mkdir(f"{path}/archives/{el[:-4]}")
            os.rename(f"{path}/{el}", f"{path}/archives/{el[:-4]}/{el}")
            shutil.unpack_archive(f"{path}/archives/{el[:-4]}/{el}", f"{path}/archives/{el[:-4]}")
            os.remove(f"{path}/archives/{el[:-4]}/{el}")
        for el in gz:
            os.mkdir(f"{path}/archives/{el[:-3]}")
            os.rename(f"{path}/{el}", f"{path}/archives/{el[:-3]}/{el}")
            shutil.unpack_archive(f"{path}/archives/{el[:-3]}/{el}", f"{path}/archives/{el[:-3]}")
            os.remove(f"{path}/archives/{el[:-3]}/{el}")
        for el in tar:
            os.mkdir(f"{path}/archives/{el[:-4]}")
            os.rename(f"{path}/{el}", f"{path}/archives/{el[:-4]}/{el}")
            shutil.unpack_archive(f"{path}/archives/{el[:-4]}/{el}", f"{path}/archives/{el[:-4]}")
            os.remove(f"{path}/archives/{el[:-4]}/{el}")


def recursiv_print(path):
    if path.is_dir():
        for element in path.iterdir():
            recursiv_print(element)
        if path.name=="images" or path.name=="audio" or path.name=="archives" or path.name=="documents" or path.name=="video":
            pass
        else:
            filterDir(path)
            #os.rename(path.name, normalize(path.name))
            if len(os.listdir(path)) == 0:
                shutil.rmtree(path)

def main():
    if len(sys.argv) <2:
        print("Error way, please try again")
    else:
        user_input = sys.argv[1]
        path = pathlib.Path(user_input)
        recursiv_print(path)


if __name__ == "__main__":
    main()
