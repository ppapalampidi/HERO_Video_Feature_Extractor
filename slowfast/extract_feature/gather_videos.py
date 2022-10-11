import copy
import os
import argparse
import json
import glob
COMMON_VIDEO_ETX = set([
    ".webm", ".mpg", ".mpeg", ".mpv", ".ogg",
    ".mp4", ".m4p", ".mpv", ".avi", ".wmv", ".qt",
    ".mov", ".flv", ".swf"])


def main(opts):
    videopath = opts.video_path
    feature_path = opts.feature_path
    csv_folder = opts.csv_folder
    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)
    # if not os.path.exists(feature_path):
    #     os.mkdir(feature_path)

    partitions = 5
    outputfiles = [f"{csv_folder}/summscreen_resnet_info_1.csv", f"{csv_folder}/summscreen_resnet_info_2.csv",
                   f"{csv_folder}/summscreen_resnet_info_3.csv", f"{csv_folder}/summscreen_resnet_info_4.csv",
                   f"{csv_folder}/summscreen_resnet_info_5.csv"]

    movies = []
    cnt = 0
    for x in os.walk(videopath):
        cnt += 1
        if cnt == 1:
            continue
        movies.append(x[0])
        # if cnt > 3:
        #     break
    print(cnt)

    for partition in range(partitions):

        partition_range = int(len(movies)/5)

        print(partition_range)

        valid_nums = [partition_range*partition, (partition_range)*(partition+1)]

        if partition_range == 4:
            valid_nums[1] = len(movies)

        print(valid_nums)
        # outputFile = f"{csv_folder}/summscreen_info.csv"
        outputFile = outputfiles[partition]

        with open(outputFile, "w") as fw:
            fw.write("video_path,feature_path\n")
            fileList = []
            # movies = [x[0] for x in os.walk(videopath)][1:]
            for z, movie in enumerate(movies):
                if z < valid_nums[0] or z >= valid_nums[1]:
                    continue
                # movie_scenes = [x[0] for x in os.walk(movie)][1:]
                # for movie_scene in movie_scenes:
                #     segs_list = sorted(glob.glob(os.path.join(movie_scene, '*.mp4')))
                #     fileList.extend(segs_list)
                segs_list = sorted(
                    glob.glob(os.path.join(movie, '*.mp4')))
                # fileList.extend(segs_list)

                fileList = copy.deepcopy(segs_list)
                if fileList == []:
                    continue

                video_name = movie.split('/')[-1]
                feature_path_now = os.path.join(feature_path, video_name)

                # if not os.path.exists(feature_path_now):
                #     os.mkdir(feature_path_now)
                for input_filename in fileList:
                    # if ',' in input_filename:
                        # input_filename = input_filename.replace(',',' ')
                    filename = os.path.basename(input_filename)
                    fileId, _ = os.path.splitext(filename)

                    output_filename = os.path.join(
                        feature_path_now, fileId+".npz")
                    # if not os.path.exists(output_filename):
                    # fw.write(input_filename+","+output_filename+"\n")
                    if not os.path.exists(output_filename):
                        fw.write(input_filename+","+output_filename+"\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("--video_path", default="/home/s1837267/new_organised_movie_data/TESTSET_video_shots/", type=str,
    #                     help="The input video path.")
    # parser.add_argument("--feature_path", default="/home/s1837267/new_organised_movie_data/TESTSET_updated_video_features/resnet_features/",
    #                     type=str, help="output feature path.")
    parser.add_argument("--video_path", default="/home/s1837267/SummScreen_data/shots/", type=str,
                        help="The input video path.")
    parser.add_argument("--feature_path", default="/home/s1837267/SummScreen_data/video_features/resnet_features/",
                        type=str, help="output feature path.")
    parser.add_argument(
        '--csv_folder', type=str, default="/home/s1837267/code/HERO_Video_Feature_Extractor/",
        help='output csv folder')
    args = parser.parse_args()
    main(args)