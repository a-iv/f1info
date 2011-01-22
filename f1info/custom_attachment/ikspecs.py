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
    height = 55

class TopDisplay(processors.Resize):
    width = 374
    height = 250


class Thumb(ImageSpec):
    pre_cache = True
    processors = [ThumbDisplay, ]

class Mini(ImageSpec):
    pre_cache = True
    processors = [MiniDisplay, ]
    quality = 95

class Top(ImageSpec):
    pre_cache = True
    processors = [TopDisplay, ]
    quality = 95