from pathlib import Path
from time import sleep

import m3u8
from urllib.parse import urlparse, urljoin
from urllib.request import urlretrieve, pathname2url
from mysite import settings

def download_m3u8_files(url_str, dest_dir):
    url = urlparse(url_str)
    m3u8_root = url.path
    m3u8_host_url = url.scheme+'://'+url.netloc
    m3u8_full_path = Path(dest_dir)/Path(m3u8_root[1:])
    m3u8_full_path.parent.mkdir(parents=True, exist_ok=True)
    file_path, message=urlretrieve(url_str, str(m3u8_full_path))
    with m3u8_full_path.open() as m3u8_file:
        m3u8_obj = m3u8.loads(m3u8_file.read())
        for ts_file in m3u8_obj.files:
            ts_url = urljoin(m3u8_host_url, pathname2url(str(Path(m3u8_root).parent / Path(ts_file))))
            ts_full_path = m3u8_full_path.parent / Path(ts_file)
            ts_full_path.parent.mkdir(parents=True, exist_ok=True)
            download_ts_file(ts_url, str(ts_full_path))

def download_ts_file(url, dest_path):
    retry = 5
    while retry:
        try:
            urlretrieve(url, str(dest_path))
            return
        except Exception as e:
            print(url+' download failed! ',e)
            sleep(1)
            retry -= 1

if __name__ == '__main__':
    download_m3u8_files('http://localhost:80/m3u8/stream1.m3u8',settings.RECORD_MEDIA_ROOT)
