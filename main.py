import argparse
import filter
from filter_implementations import Brightness, Hue
import ui
import video_controller_ui
def main(args):
    vf = filter.VideoFilter();
    vf.addFilter(Brightness())
    vf.addFilter(Hue())

    #vf.selectVideo("data/outcpp.avi")

    #vf.previewVideo()
    vc = video_controller_ui.VideoController(vf)
    ui_ = video_controller_ui.VideoUI(vc, 0)
    ui_.main()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Filter")
    args = parser.parse_args()
    print(args)
    main(args)