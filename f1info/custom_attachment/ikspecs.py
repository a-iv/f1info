# -*- coding: utf-8 -*-

from imagekit import processors
from imagekit.specs import ImageSpec

class ResizeDisplay(processors.Resize):
    width = 800
    height = 800

class Display(ImageSpec):
    processors = [ResizeDisplay, ]

class ThumbDisplay(processors.Resize):
    width = 80
    height = 80

class MiniDisplay(processors.Resize):
    width = 48
    height = 48
    crop = True

class ArticlesDisplay(processors.Resize):
    width = 65
    height = 65
    crop = True

class TopDisplay(processors.Resize):
    width = 320

class HeatDisplay(processors.Resize):
    width = 266


class Thumb(ImageSpec):
    pre_cache = True
    processors = [ThumbDisplay, ]

class Mini(ImageSpec):
    crop = ('center',)    
    pre_cache = True
    processors = [MiniDisplay, ]
    quality = 95

class Articles(ImageSpec):
    crop = ('center',)    
    pre_cache = True
    processors = [ArticlesDisplay, ]
    quality = 95

class Top(ImageSpec):
    pre_cache = True
    processors = [TopDisplay, ]
    quality = 95

class Heat(ImageSpec):
    pre_cache = True
    processors = [HeatDisplay, ]
    quality = 95
