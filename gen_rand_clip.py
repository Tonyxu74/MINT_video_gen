from moviepy101.moviepy.editor import concatenate_videoclips, VideoFileClip
import numpy as np


# writes a file to the file path with the given text
def write_file(file_path, text):
    f = open(file_path, "a+")
    f.write(text)
    f.close()


# NOTE THE FINAL BLINK IS AT 13s
def gen_clip(vid_path, name, max_time=7, min_time=3, video_length=20):
    '''
    Author: Tony Xu
    Generates a video clip for the Flanker test
    DELETES file if similar path exists!!
    :param vid_path: path to save video and log of video
    :param max_time: the maximum length of the flashing clips
    :param min_time: the minimum length of the flashing clips
    :param video_length: the number of flashing highlighted clips
    :return: none
    '''

    c1 = VideoFileClip('./leftarm.mp4').subclip(t_start=0, t_end=max_time)
    c2 = VideoFileClip('./leftleg.mp4').subclip(t_start=0, t_end=max_time)
    c3 = VideoFileClip('./rightarm.mp4').subclip(t_start=0, t_end=max_time)
    c4 = VideoFileClip('./rightleg.mp4').subclip(t_start=0, t_end=max_time)
    null = VideoFileClip('./alloff.mp4').subclip(t_start=0, t_end=max_time)
    init = VideoFileClip('./init_clip.mp4').subclip(t_start=0, t_end=15)

    clips = [c1, c2, c3, c4]
    clip_log = []
    cliplist = [init]
    # the length of the initial clip is 15 seconds
    time_in_video = 15

    for i in range(video_length):

        # generate a random clip length for the NULL clip and append it, also increase the time in the video
        null_length = np.random.randint(low=min_time, high=max_time+1)
        cliplist.append(null.subclip(t_start=0, t_end=null_length))
        time_in_video += null_length

        # generate a random clip number
        rand_clip_num = np.random.randint(low=0, high=4)
        r_clip = clips[rand_clip_num]

        # generate a random clip length for the HIGHLIGHTED clip
        hl_length = np.random.randint(low=min_time, high=max_time+1)

        # note the start of the clip and length of the clip
        clip_log.append({
            'clip_number': rand_clip_num,
            'time': time_in_video,
            'length': hl_length
        })

        # now append the random clip and add the length of the time to the total video time
        r_clip = r_clip.subclip(t_start=0, t_end=hl_length)
        cliplist.append(r_clip)
        time_in_video += hl_length

    # now just save the video
    final_clip = concatenate_videoclips(cliplist)
    final_clip.write_videofile('./{}.mp4'.format(vid_path))

    # and save the clip log in a txt NOTE THIS DELETES THE PREVIOUS FILE!!
    f = open('{}_log.txt'.format(vid_path), 'w')
    f.close()
    write_file('{}_log.txt'.format(vid_path), 'clip_num(0:leftarm, 1:leftleg, 2:rightarm, 3:rightleg) | time_in_video | length_of_clip\n')
    write_file('{}_log.txt'.format(vid_path), 'experiment conducted by: {}\n'.format(name))
    write_file('{}_log.txt'.format(vid_path), '-----Note: final blink is at 13 seconds-----\n')
    for clip in clip_log:
        write_file('{}_log.txt'.format(vid_path), '{} {} {}\n'.format(clip['clip_number'], clip['time'], clip['length']))


if __name__ == '__main__':
    gen_clip('nov16_clip3', 'Riley')
