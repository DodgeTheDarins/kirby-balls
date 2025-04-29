from mutagen.flac import Picture, FLAC, error as FLACError
from mutagen.oggopus import OggOpus
from pathlib import Path
import subprocess
import base64
import shutil
import glob
import os

def extract_cover(file,output):
    file_ = OggOpus(file)

    for b64_data in file_.get("metadata_block_picture", []):
        try:
            data = base64.b64decode(b64_data)
        except (TypeError, ValueError):
            continue

        try:
            picture = Picture(data)
        except FLACError:
            continue

        extensions = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
        }
        ext = extensions.get(picture.mime, "png")

        with open(f"{output}.%s" % ext, "wb") as h:
            h.write(picture.data)
            print("exctract")
            
def extract_cover_flac(file,output):
    var = FLAC(file)
    pics = var.pictures
    print(pics)
    for p in pics:
        if p.type == 3:
            with open(output, "wb") as f:
                f.write(p.data)

Path("./wav/").mkdir(parents=True, exist_ok=True)
files_to_convert_ogg = glob.glob("*.ogg")
files_to_convert_flac = glob.glob("*.flac")
files_to_copy = glob.glob("*.mp3")
# for file in files_to_convert_ogg:
#     print(file)
#     filenew = os.path.basename(str(file))
#     filenew, extension = os.path.splitext(filenew)
#     extract_cover(file, filenew)
#     if os.path.isfile(f'{filenew}.png'):
#         subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, '-i', f'{filenew}.png', '-c:v', 'mjpeg', '-b:a', "320000",'-id3v2_version', '3', '-metadata:s:v', 'title="Album cover"', '-metadata:s:v', 'comment="Cover (front)"', f'.\\mp3\\{filenew}.mp3'])
#         os.remove(f'{filenew}.png')
#     elif os.path.isfile(f'{filenew}.jpg'):
#         subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, '-i', f'{filenew}.jpg', '-c:v', 'mjpeg', '-b:a', "320000",'-id3v2_version', '3', '-metadata:s:v', 'title="Album cover"', '-metadata:s:v', 'comment="Cover (front)"', f'.\\mp3\\{filenew}.mp3'])
#         os.remove(f'{filenew}.jpg')
#     else:
#         subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, '-b:a', "320000", f'.\\mp3\\{filenew}.mp3'])
        
# for file in files_to_convert_flac:
#     filenew = os.path.basename(str(file))
#     filenew, extension = os.path.splitext(filenew)
#     extract_cover_flac(file,filenew)
#     if os.path.isfile(f'{filenew}'):
#         subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, '-i', f'{filenew}', '-c:v', 'mjpeg', '-b:a', "320000",'-id3v2_version', '3', '-metadata:s:v', 'title="Album cover"', '-metadata:s:v', 'comment="Cover (front)"', f'.\\mp3\\{filenew}.mp3'])
#         os.remove(f'{filenew}')
#     else:
#         subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, '-b:a', "320000", f'.\\mp3\\{filenew}.mp3'])
    
for file in files_to_copy:
    filenew = os.path.basename(str(file))
    filenew, extension = os.path.splitext(filenew)
    if os.path.isfile(f'{filenew}'):
        subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, '-i', f'{filenew}', '-c:v', 'mjpeg', '-b:a', "320000",'-id3v2_version', '3', '-metadata:s:v', 'title="Album cover"', '-metadata:s:v', 'comment="Cover (front)"', f'.\\wav\\{filenew}.wav'])
        os.remove(f'{filenew}')
    else:
        subprocess.run(['ffmpeg', '-hide_banner','-y', '-i', file, f'.\\wav\\{filenew}.wav'])    
    print(file)