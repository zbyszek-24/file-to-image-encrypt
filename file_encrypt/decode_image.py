

from PIL import Image
import numpy

def get_pixel_data(filepath):
    '''
    This function gets all the color data from the image and converts the RGB values into 1 long list.
    Thanks to stack overflow for the numpy transformation.
    :param filepath: filepath of the image
    :return: RGB_values
    '''
    with Image.open(filepath) as img:
        colors = img.getdata()
        width, height = img.size
        pixel_data = numpy.array(colors).reshape(width,height,3)
    RGB_values = []
    # append individual integers to the RGB values list.
    for row in pixel_data:
        for pixel in row:
            for channel in pixel:
                RGB_values.append(int(channel))
    return RGB_values

def get_length_and_extension(RGB_values):
    '''
    This function reads the amount of bytes and the file extension encoded in the data and returns them
    :param RGB_values:
    :return:
    '''
    byte_length_RGB = []
    file_extension_RGB = []
    # First 3 bytes = byte length, next 6 bytes = file extension
    for i in range(0,9):
        if i <=2:
            byte_length_RGB.append(RGB_values[i])
        else:
            if RGB_values[i] != 0:
                file_extension_RGB.append(RGB_values[i])
            #if the bytes=0 that means they are null characters, and the file extension has ended
            else:
                break
    byte_number = int.from_bytes(byte_length_RGB, 'big')
    file_extension = bytearray(file_extension_RGB).decode()
    return byte_number, file_extension
def save_file(RGB_values, byte_number, filepath, file_extension):
    '''
    Writes to a new file using the ive filepath, the decoded extension and the decoded data
    :param RGB_values:
    :param byte_number:
    :param filepath:
    :param file_extension:
    :return:
    '''
    #cut the first 3 integers from the list, up until the byte number we received +6 (because we cut out the first 6 integers)
    extracted_bytes = RGB_values[6:byte_number+6]
    #save file
    with open(f'{filepath}.{file_extension}', 'wb') as file:
        bytes_to_write = bytearray(extracted_bytes)
        file.write(bytes_to_write)


if __name__ == '__main__':
    RGB_values = get_pixel_data(input('Filepath of file to decode: '))
    byte_number, file_extension = get_length_and_extension(RGB_values)
    print('Write down the path to where you want to save the file.')
    filepath = input('Example: home/user/Desktop/new_file \n')
    save_file(RGB_values, byte_number, filepath, file_extension)
