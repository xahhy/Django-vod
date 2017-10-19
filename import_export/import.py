import json
from pathlib import Path
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
PackFolder = 'video_pack'
VideosFolder = 'videos'
ImagesFolder = 'images'
DescriptionsFolder = 'descriptions'
if __name__ == '__main__':
    videos = []
    videos_path = Path(PackFolder)/Path(VideosFolder)
    for path in videos_path.glob('*'):
        if path.is_dir():
            print(path.name)
        else:
            videos.append(path)
    # with Path('./description.txt').open(encoding='utf-8') as f:
    #     text = f.read()
    #     print(text)
        # JsonInfo = json.loads(text)
        # for item in JsonInfo:
        #     print(item)
