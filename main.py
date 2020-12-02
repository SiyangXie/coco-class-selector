import argparse
import utils
import yaml


def generate():
    config = yaml.load(open(opt.cfg), Loader=yaml.FullLoader)

    if opt.do == 'filter':
        utils.coco_filter(label_num=opt.n, config=config)
    if opt.do == 'split':
        utils.coco_split(config=config)
    if opt.do == 'concat':
        utils.concat_label(config=config)
    if opt.do == 'match':
        utils.label_match_image(config=config)
    if opt.do == 'rename':
        utils.rename(config=config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', type=str, default='filter', help='[filter, split, concat, match, rename]')
    parser.add_argument('--n', type=str, default='-1', help='num of labels selected')
    parser.add_argument('--cfg', type=str, default='.\\config.yaml', help='config yaml folder')

    opt = parser.parse_args()

    generate()
    # # python main.py --do filter --n 1000
    # # python main.py --do split
