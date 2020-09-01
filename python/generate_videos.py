import numpy as np
import glob
import cv2
import os
from PIL import Image


def sort_files(input_path, frmt='png', print_names=False):
    # load filenames
    filenames = glob.glob(input_path+'*.'+frmt)
    print("number of files: {}".format(len(filenames)))
    # custom sorting function
    filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if print_names:
        for f in filenames:
            print(f)
    return filenames

def load_tifs(path):
    retval, mats = cv2.imreadmulti(path)
    mats = np.array(mats)
    return retval, mats

def write_video(images, output_path, video_name, frame_rate, frmt, is_rgb):
    img_shape = images[0].shape[:2]
    print("Output video shape: {}".format(img_shape))
    # create videowriter
    if frmt=="mp4":
        out = cv2.VideoWriter(output_path+video_name+'.mp4', cv2.VideoWriter_fourcc(*'MP4V'), frame_rate, img_shape, is_rgb)
    elif frmt=="avi":
        out = cv2.VideoWriter(output_path+video_name+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, img_shape, is_rgb)
    # write images to video
    for i in range(images.shape[0]):
        out.write(images[i])
    out.release()
    print("Successfully created "+frmt+" video")

def create_video_from_pngs(filenames, output_path, video_name, frame_rate=10, frmt="mp4", is_rgb=False):
    # extract image from filename and store as a numpy array
    images = []
    for f in filenames:
        im = Image.open(f)
        im = np.array(im)
        images.append(im)
    images = np.array(images)
    print("Images shape: {}".format(images.shape))
    write_video(images, output_path, video_name, frame_rate, frmt, is_rgb)

def create_video_from_tifs(filenames, output_path, video_name, frame_rate=10, frmt="mp4", is_rgb=False):
    images=[]
    for f in filenames:
        _, img = load_tifs(f)
        images.append(np.squeeze(img))
    images = np.array(images)
    print("Images shape: {}".format(images.shape))
    write_video(images, output_path, video_name, frame_rate, frmt, is_rgb)

def create_video_from_npy(filenames, output_path, video_name, frame_rate=10, frmt="mp4", is_rgb=False):
    filename = filenames[0] # get the file you want
    images = np.load(filename)
    print("Images shape: {}".format(images.shape))
    write_video(images, output_path, video_name, frame_rate, frmt, is_rgb)

    
def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
    return True


if __name__ == '__main__':

    # set input path and output paths
    input_path = '../data/npy/'
    output_path = '../outputs/'
    video_name = 'npys'

    # sort files
    filenames = sort_files(input_path, frmt='npy', print_names=False)
    # select video creation operation
    # create_video_from_pngs(filenames, output_path, video_name, 10, frmt="avi", is_rgb=False)
    # create_video_from_tifs(filenames, output_path, video_name, 10, frmt="mp4", is_rgb=False)
    create_video_from_npy(filenames, output_path, video_name, 10, frmt="avi", is_rgb=False)
    
    # convert AVI to MP4
    convert = True
    avi_file_path = '../outputs/npys.avi'
    mp4_video_name = video_name+'_mp4'
    if convert:    
        convert_avi_to_mp4(avi_file_path, output_path+mp4_video_name)