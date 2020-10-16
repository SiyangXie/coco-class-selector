import argparse
import utils


def generate():
    filtered_label = utils.filter_label(slabel=opt.sl, dlabel=opt.dl, lnum=opt.lnum)
    utils.filter_img(simage=opt.si, slabel=filtered_label, dimage=opt.di)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--net', type=str, default='yolov3', help='[yolov3, yolov5]')
    parser.add_argument('--lnum', type=str, default='-1', help='num of labels selected')

    parser.add_argument('--si', type=str, default='.\\input\\images', help='source image folder')
    parser.add_argument('--di', type=str, default='.\\output\\images', help='dest image folder')

    parser.add_argument('--sl', type=str, default='.\\input\\labels', help='source label folder')
    parser.add_argument('--dl', type=str, default='.\\output\\labels', help='dest label folder')

    parser.add_argument('--config', type=str, default='.\\', help='config yaml folder')

    opt = parser.parse_args()

    generate()

    # python main.py - -sl D:\BaiduNetdiskDownload\coco2014\labels\train2014 - -dl
    # D:\BaiduNetdiskDownload\coco2014_filtered\labels
