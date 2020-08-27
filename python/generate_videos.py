import numpy as np
import glob
import cv2
import os
from PIL import Image


def sort_files(input_path, print_names=False):
    # load filenames
    filenames = glob.glob(input_path+'*.png')
    # custom sorting function
    filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if print_names:
        for f in filenames:
            print(f)
    return filenames

def create_video_from_pngs(filenames, output_path, video_name, frame_rate=10, frmt="mp4"):
    # extract image from filename and store as a numpy array
    images = []
    for f in filenames:
        im = Image.open(f)
        im = np.array(im)
        images.append(im)
    images = np.array(images)
    print("Images shape: {}".format(images[0].shape))
    img_shape = images[0].shape[:2]
    print("Output video shape: {}".format(img_shape))
    # create videowriter
    if frmt=="mp4":
        out = cv2.VideoWriter(output_path+video_name+'.mp4', cv2.VideoWriter_fourcc(*'MP4V'), frame_rate, img_shape, 0)
    elif frmt=="avi":
        out = cv2.VideoWriter(output_path+video_name+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, img_shape, 0)
    # write images to video
    for i in range(images.shape[0]):
        out.write(images[i])
    out.release()
    print("Successfully created "+frmt+" video")

# under construction
def create_video_from_tifs(input_path, output_path):
    mats = load_maxprojections(input_path, save=False)
    print("mats shape: {}".format(mats.shape))
    s = mats.shape[1]
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 5, (s,s), 0)
    for i in range(mats.shape[0]):
        out.write(mats[i])
    out.release()
    print("Done")

# under construction
def create_video_from_mats(mats_path, video_path):
    mats = np.load(mats_path)
    print(mats.shape)
    writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (512,512))
    for i in range(mats.shape[0]):
        writer.write(mats[i])
    writer.release()
    
def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
    return True


if __name__ == '__main__':

    # set input path and output paths
    input_path = '../data/pngs/'
    output_path = '../outputs/'
    video_name = 'pngs'

    # sort files
    filenames = sort_files(input_path, print_names=False)

    # select video creation operation
    create_video_from_pngs(filenames, output_path, video_name, 10, frmt="avi")
    # create_video_from_tifs(input_path, output_path)
    # create_video_from_mats(mats_path, video_path)
    
    # convert AVI to MP4
    avi_file_path = '../outputs/pngs.avi'
    mp4_video_name = video_name+'_mp4'
    convert_avi_to_mp4(avi_file_path, output_path+mp4_video_name)