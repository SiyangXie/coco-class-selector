import argparse
import utils


def generate():
    net, src_i, src_l, dst = opt.net, opt.src_img, opt.src_label, opt.dst

    utils.filter_label(src_l, c='0')
    utils.filter_img(idir=src_i, ldir=src_l, idst=dst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--net', type=str, default='yolov3', help='[yolov3, yolov5]')
    parser.add_argument('--src-img', type=str, default='.\\', help='source image folder')
    parser.add_argument('--src-label', type=str, default='.\\', help='source label folder')
    parser.add_argument('--dst', type=str, default='.\\output', help='dest folder')
    opt = parser.parse_args()

    generate()
