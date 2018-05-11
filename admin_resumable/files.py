# -*- coding: utf-8 -*-
import logging
import os
import re
import zipfile
from pathlib import Path
from django.core.files.base import File
from django.conf import settings
from vodmanagement import models
from datetime import datetime

class ResumableFile(object):
    def __init__(self, storage, kwargs):
        self.storage = storage
        self.kwargs = kwargs
        self.chunk_suffix = "_part_"
        self.video_allow = getattr(settings, 'ADMIN_RESUMABLE_VIDEO_ALLOW', ['.mp4', '.mkv' '.avi', '.rmvb', 'mpeg', '.mov'])
        self.image_allow = getattr(settings, 'ADMIN_RESUMABLE_IMAGE_ALLOW', ['.jpg', '.jpeg', '.png', '.bmp', '.gif'])

    @property
    def chunk_exists(self):
        """Checks if the requested chunk exists.
        """
        return self.storage.exists(self.current_chunk_name) and \
               self.storage.size(self.current_chunk_name) == int(self.kwargs.get('resumableCurrentChunkSize'))

    @property
    def chunk_names(self):
        """Iterates over all stored chunks.
        """
        files = sorted(self.storage.listdir('')[1])
        chunks = [file for file in files if str(file).startswith('%s%s' % (self.filename, self.chunk_suffix))]
        return chunks

    @property
    def current_chunk_name(self):
        return "%s%s%s" % (
            self.filename,
            self.chunk_suffix,
            self.kwargs.get('resumableChunkNumber').zfill(4)
        )

    def chunks(self):
        """Iterates over all stored chunks.
        """
        chunks = []
        files = sorted(self.storage.listdir('')[1])
        for file in files:
            if str(file).startswith('%s%s' % (self.filename, self.chunk_suffix)):
                yield self.storage.open(file, 'rb').read()

    def delete_chunks(self):
        [self.storage.delete(chunk) for chunk in self.chunk_names]

    @property
    def file(self):
        """Gets the complete file.
        """
        if not self.is_complete:
            raise Exception('Chunk(s) still missing')

        return self

    @property
    def filename(self):
        """Gets the filename."""
        filename = self.kwargs.get('resumableFilename')
        self.base_filename = filename
        if '/' in filename:
            raise Exception('Invalid filename')
        return filename
        #     self.kwargs.get('resumableTotalSize'),
        #     filename
        # )

    @property
    def is_complete(self):
        """Checks if all chunks are already stored.
        """
        return int(self.kwargs.get('resumableTotalSize')) == self.size

    def process_chunk(self, file):
        if self.storage.exists(self.current_chunk_name):
            self.storage.delete(self.current_chunk_name)
        self.storage.save(self.current_chunk_name, file)

    @property
    def size(self):
        """Gets chunks size.
        """
        size = 0
        for chunk in self.chunk_names:
            size += self.storage.size(chunk)
        return size

    def resotre_file(self):
        zip_file = Path(self.storage.location)/Path(self.base_filename)
        logging.debug('开始解压文件',zip_file)
        file_zip = zipfile.ZipFile(zip_file, 'r')
        for file in file_zip.namelist():
            file_zip.extract(file, self.storage.location)
        file_zip.close()
        logging.debug('解压文件完成',self.storage.location)
        os.remove(file_zip.filename)

    def save_model(self, model, save_path, request):
        category_id = request.POST['category']
        if category_id is '':
            category_id = models.VideoCategory.objects.first().id
        logging.debug("multiple category is ", category_id)
        (short_name, extension) = os.path.splitext(os.path.basename(self.base_filename))
        file_url = Path(self.storage.base_url).relative_to(settings.MEDIA_URL) / self.base_filename
        obj = model.objects.filter(title=short_name)
        if extension.lower() in self.video_allow:
            if obj:
                obj.update(video=file_url)
                logging.debug("obj exists , update video")
            else:
                obj = model(title=short_name, save_path=save_path, category=models.VideoCategory.objects.get(id=category_id))
                obj.video.name = file_url
                obj.save()
                logging.debug("model video name=", obj.video.name)
                logging.debug("video save model done:", self.filename)

        if extension.lower() in self.image_allow:
            if obj:
                obj.update(image=file_url)
                logging.debug("obj exists , update image")
            else:
                obj = model(title=short_name, save_path=save_path, category=models.VideoCategory.objects.get(id=category_id))
                obj.image.name = file_url
                obj.save()
                logging.debug("model image name=", obj.image.name)
                logging.debug("image save model done:", self.filename)

