import subprocess
import re
import asyncio

import mimetypes

output_path = "./bot/OUTPUTS/generated_video.mp4"


def get_video_duration(video_path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout)


async def create_video(v_path, a_path, v_loop, a_loop):
    vid_cmd = f'ffmpeg -stream_loop {v_loop} -i "{v_path}" -stream_loop {a_loop} -i "{a_path}" ' + \
        f'-c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 -shortest -vf "fade=t=in:st=0:d=5" "{output_path}"'

    photo_cmd = f'ffmpeg -loop 1 -i "{v_path}" -stream_loop {a_loop} -i "{a_path}" ' +\
        f'-c:v libx264 -tune stillimage -c:a aac -shortest -pix_fmt yuv420p "{output_path}"'

    video = is_video(v_path)
    cmd = vid_cmd if video else photo_cmd

    cmd = f'ffmpeg -stream_loop {v_loop} -i "{v_path}" -stream_loop {a_loop} -i "{a_path}" ' + \
        f'-c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest "{output_path}"'
    

    task = await asyncio.create_subprocess_shell(cmd)
    #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout, stderr = process.communicate()

    await task.wait()

    return output_path


def is_video(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")