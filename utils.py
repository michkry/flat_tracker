from PIL import ImageTk, Image

# Returns a dictionary with literals from provided file
# Example of usage: getLiteralsDict("literals.txt", "=")
def get_literals_dict(literals_file_name, separator):
    literalsFile = open(literals_file_name)
    literalsDict = {}
    for line in literalsFile.readlines():
        equalsSignPos = line.find(separator)
        literalsDict[line[0:equalsSignPos]
                     .strip()]=line[equalsSignPos+1:].strip()
    literalsFile.close()
    return literalsDict

# Returns an image from provided path
def get_image(img_path):
    return ImageTk.PhotoImage(Image.open(img_path))

# Resizes provided image to have provided width and height
def resize_image(img_path, width, height):
    size = width, height
    out_img = "temp"
    try:
        im = Image.open(img_path)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(out_img, "JPEG")
    except IOError as ex:
        print (ex)
