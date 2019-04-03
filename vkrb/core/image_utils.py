from PIL import Image, ExifTags

__EXIF_TAGS = None


def __init__():
    global __EXIF_TAGS
    __EXIF_TAGS = {}
    for key, value in ExifTags.TAGS.items():
        __EXIF_TAGS[value] = key


__init__()


def image_rotate(image: Image) -> Image:
    try:
        exif = image._getexif()
        if exif is None:
            return image

        tag_value = __EXIF_TAGS.get('Orientation')
        if tag_value is not None:
            current_orientation = exif.get(tag_value)
            if current_orientation is not None:
                angle = None
                if current_orientation == 3:
                    angle = 180
                elif current_orientation == 6:
                    angle = 270
                elif current_orientation == 8:
                    angle = 90
                if angle is not None:
                    image = image.rotate(angle, expand=True)
    except (AttributeError, IndexError) as e:
        # cases: image don't have getexif
        pass
    return image
