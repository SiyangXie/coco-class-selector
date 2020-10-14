import os
import shutil


def filter_label(ldir, c='0'):
    assert os.path.isdir(ldir), 'ERROR: --label folder does not exist'
    assert len(ldir), 'ERROR: --label folder is empty'
    for filename in os.listdir(ldir):
        with open(os.path.join(ldir, filename), 'r') as f:
            lines = f.readlines()
        with open(os.path.join(ldir, filename), 'w') as f:
            for line in lines:
                if line.strip("\n")[0] == c:
                    f.write(line)


def filter_img(idir, ldir, idst):
    for filename in os.listdir(ldir):
        base_txt = os.path.splitext(filename)[0]

        for imagename in os.listdir(idir):
            base_img = os.path.splitext(imagename)[0]

            if base_txt == base_img:
                shutil.copyfile(idir + imagename, idst + imagename)


def yolov5():
    pass


def yolov3():
    pass
