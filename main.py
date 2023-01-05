import argparse
import filter
from filter_implementations import Brightness, Hue
import ui
import video_controller_ui
import cv2
def main(args):
    vf = filter.VideoFilter();
    #vf.addFilter(Brightness("brightness", 0,100, 100))
    #vf.addFilter(Hue("hue"))
    vf.selectVideo("rtspsrc  location=rtsp://admin:admin1@192.168.1.50:554/h264Preview_01_main ! rtph264depay ! h264parse ! decodebin  ! videoconvert ! videoscale ! videorate ! video/x-raw,width=1280,height=720,framerate=5/1 ! appsink", cv2.CAP_GSTREAMER)
    #vf.previewVideo()
    vc = video_controller_ui.VideoController(vf)
    ui_ = video_controller_ui.VideoUI(vc, 0)
    ui_.main()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Filter")
    args = parser.parse_args()
    print(args)
    main(args)