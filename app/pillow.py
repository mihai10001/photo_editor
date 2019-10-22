from PIL import Image, ImageFilter, ImageEnhance


def load_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print('Unable to load image')


def get_default_slider():
    return {'color': 1, 'bright': 1, 'contrast': 1, 'sharp': 1}


# ENHANCERS
def apply_enhancers(image, image_path, slider):
    colorer = ImageEnhance.Color(image)
    image = colorer.enhance(slider['color'])
    brighter = ImageEnhance.Brightness(image)
    image = brighter.enhance(slider['bright'])
    contraster = ImageEnhance.Contrast(image)
    image = contraster.enhance(slider['contrast'])
    sharper = ImageEnhance.Sharpness(image)
    image = sharper.enhance(slider['sharp'])

    image.save(image_path)


# BLUR
def apply_blur(image_path, options):
    image = load_image(image_path)

    if options == "0":
        image = image.filter(ImageFilter.BLUR)
    elif options == "1":
        image = image.filter(ImageFilter.BoxBlur(1))
    elif options == "2":
        image = image.filter(ImageFilter.GaussianBlur)

    image.save(image_path)


# SHARPEN
def apply_sharpen(image_path, options):
    image = load_image(image_path)

    if options == "0":
        image = image.filter(ImageFilter.SHARPEN)
    elif options == "1":
        image = image.filter(ImageFilter.DETAIL)
    elif options == "2":
        image = image.filter(ImageFilter.UnsharpMask)

    image.save(image_path)


# EDGE ENHANCE
def apply_edge_enhance(image_path, options):
    image = load_image(image_path)

    if options == "0":
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    elif options == "1":
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif options == "2":
        image = image.filter(ImageFilter.EMBOSS)
    elif options == "3":
        image = image.filter(ImageFilter.FIND_EDGES)
    elif options == "4":
        image = image.filter(ImageFilter.CONTOUR)

    image.save(image_path)


# SMOOTH
def apply_smooth(image_path, options):
    image = load_image(image_path)

    if options == "0":
        image = image.filter(ImageFilter.SMOOTH)
    elif options == "1":
        image = image.filter(ImageFilter.SMOOTH_MORE)

    image.save(image_path)
