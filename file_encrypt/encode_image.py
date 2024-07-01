import PIL.Image as Image
import io
import base64
import math
import numpy


def get_widthXheight(length):
    '''
    This function takes in the length of the data and finds an optimal resolution for the embedded image
    First it takes the square root of the number, then it assigns the number rounded up to 1 var, and rounded down to another
    If the values multiplied by one another give enough space for all the data, that gets passed,
    if they don't the value that's rounded up gets passed
    :param length:
    :return: resolution
    '''
    sqrt = math.sqrt(length)
    sqrt_floor = math.floor(sqrt)
    sqrt_ceil = math.ceil(sqrt)
    if sqrt_floor * sqrt_ceil >= length:
        return (sqrt_floor, sqrt_ceil)
    else:
        return (sqrt_ceil, sqrt_ceil)


def get_RGB_from_file(filename):
    '''
    This function reads the bytes from the file, converts the number of bytes in the data and the file extension
    into an RGB value for decoding the image later. Then it makes a list of RGB values from the data and returns it.
    :param filename:
    :return: RGB_values
    '''
    # Open file and read the data as bytearray
    with (open(filename, 'rb') as file):
        data = file.read()
        bytes_from_data = bytearray(data)
    # Convert the bytes into a list of integers
    integer_list_from_bytes = list(bytes_from_data)
    # Get the length of the list of integers, convert that number into bytes, and then into a tuple of 3 integers (RGB)
    data_size_in_RGB = tuple(len(integer_list_from_bytes).to_bytes(3, 'big'))
    # Make the number of bytes divisble by 3 by adding 0's to the data. This is why we encoded the amount of data in the first RGB value
    file_extension = filename.split('.')[-1]
    file_extension_bytes = tuple(str.encode(file_extension))
    while len(file_extension_bytes) < 6:
        file_extension_bytes = file_extension_bytes + (0,)
    file_extension_bytes = (file_extension_bytes[:3], file_extension_bytes[3:])
    while len(integer_list_from_bytes) % 3:
        integer_list_from_bytes.append(0)
    RGB_values = [data_size_in_RGB, file_extension_bytes[0], file_extension_bytes[1]]
    RGB_values_temp = ()
    # Add the data into the new RGB_values list, in chunks of 3
    for integer in integer_list_from_bytes:
        RGB_values_temp = RGB_values_temp + (integer,)
        if len(RGB_values_temp) == 3:
            RGB_values.append(RGB_values_temp)
            RGB_values_temp = ()
    return RGB_values


def create_image(filename):
    '''
    This function first calls two other functions to get the data and the resolution.
    Then it creates a blank dark image of the calculated resolution and embeds the data.
    Finally it shows the image to the user.
    :return: status
    '''
    data = get_RGB_from_file(filename)
    print(data)
    resolution = get_widthXheight(len(data))
    with Image.new(mode='RGB', size=resolution) as image:
        image.putdata(data)
        image.show()
        image.save('aaa_img_test_final.png', 'PNG')


def get_RGB_from_image(filepath):
    '''

    :param filepath:
    :return:
    '''
    embedded_image = Image.open(filepath).load()
    width, height = Image.size(filepath)
    a = embedded_image[10, 10]


if __name__ == '__main__':
    filepath = input('Filepath of file to embed: ')
    create_image(filepath)