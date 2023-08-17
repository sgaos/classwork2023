from tkinter import filedialog
import base64
import requests
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

# select image to upload
def select_image():
    filename = filedialog.askopenfilename()
    return filename

def read_file_as_b64(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string

def post_b64string_image(b64_string):
    in_data = {"image": b64_string, "net_id": "sg622", "id_no": 1}
    r = requests.post("http://vcm-21170.vm.duke.edu", json = in_data)
    print(r.text)
    print(r.status_code)

def get_b64_string_image():
    r = requests.get("http://vcm-21170.vm.duke.edu"+"/get_image/sg622/1")
    return r.text

def save_b64_to_image(b64_string):
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return

def main():
    filename = select_image()
    if filename == "":
        return
    b64_string = read_file_as_b64(filename)
    post_b64string_image(b64_string)

    b64_string_from_server = get_b64_string_image()
    save_b64_to_image(b64_string_from_server)


if __name__ == '__main__':
    main()






