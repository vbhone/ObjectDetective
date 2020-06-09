from django.shortcuts import render
from PIL import Image
# Create your views here.
from app.yolo import YOLO
import glob
from app.models import Img
def index(request):
    return render(request,"index.html")


def predict(request):
    context=[]
    yolo=YOLO()
    if request.method == 'POST':
        image=request.FILES.get('img')
    # path_file_number = str(len(glob.glob(pathname='/static/images/*.jpg')) + 1)
    # input_file = "/static/images/" + path_file_number + ".jpg"
    image=Img(img_url=image)
    image.save()
    #
    # image.save(input_file)
    # input_file=image.img_url.url
    # input_file="/static/images/about-img.jpg"
    print(image.img_url)
    r_image = yolo.detect_image(Image.open(image.img_url.url))

    # r_image.show()
    path_file_number = str(len(glob.glob(pathname='./app/static/out/*.jpg')) + 1)
    # print("filename  ", path_file_number)
    filename="./app/static/out/" + path_file_number + ".jpg"
    r_image.save(filename)
    retfile="static/out/" + path_file_number + ".jpg"
    input_file=image.img_url.url.replace("app/static","static")
    # context.append(input_file)
    context={
        "img":input_file,
        "predict":retfile
    }
    # yolo.close_session()
    return render(request,"index.html",context)