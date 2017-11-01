import json
from pathlib import Path

VIDEO_FOLDER = '../video_pack'
IMAGE_SUFFIX = ['.jpg', '.png', '.jpeg', '.bmp']

if __name__ == '__main__':
    json_list = []
    video_path = Path(VIDEO_FOLDER)
    videos = video_path.rglob('*.mp4')
    for video in videos:
        title,_ = video.name.split('.')
        video = video.relative_to(video_path)
        definition = 'SD'
        save_path = 'default'
        json_video = {}
        json_video['title'] = title
        json_video['video'] = str(video)
        json_video['definition'] = definition
        json_video['save_path'] = save_path
        json_list.append(json_video)

    with open('./dumps.txt','w') as f:
        f.write(json.dumps(json_list))


    #
    # for suffix in IMAGE_SUFFIX:
    #     images = video_path.rglob('*%s' % suffix)
    #     print(list(images))