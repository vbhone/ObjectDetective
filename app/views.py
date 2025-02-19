from django.shortcuts import render
from PIL import Image
# Create your views here.
from app.yolo import YOLO
import glob
from app.models import Img
import keras.backend as K
import random
def index(request):
    context={}
    number=set()
    j=1
    photo = glob.glob("./app/static/out/*.jpg")
    path_file_number = len(photo)
    while len(number) < 3:
        a = random.randint(0, path_file_number-1)
        number.add(a)
    for i in number:
        context["photo"+str(j)]="/static/out/"+str(photo[i].split("\\")[-1])
        j+=1
    print(context)

    return render(request,"index.html",context)


def predict(request):
    context=[]
    yolo=YOLO()
    if request.method == 'POST':
        image=request.FILES.get('img')
    # path_file_number = str(len(glob.glob(pathname='/static/images/*.jpg')) + 1)
    # input_file = "/static/images/" + path_file_number + ".jpg"
    image=Img(img_url=image)
    image.save()
    print(image.img_url)
    r_image = yolo.detect_image(Image.open(image.img_url.url))

    path_file_number = str(len(glob.glob(pathname='./app/static/out/*.jpg')) + 1)
    filename="./app/static/out/" + path_file_number + ".jpg"
    r_image.save(filename)
    retfile="static/out/" + path_file_number + ".jpg"
    input_file=image.img_url.url.replace("app/static","static")
    context={
        "img":input_file,
        "predict":retfile
    }

    number = set()
    j = 1
    photo = glob.glob("./app/static/out/*.jpg")
    path_file_number = len(photo)
    while len(number) < 3:
        a = random.randint(0, path_file_number - 1)
        number.add(a)
    for i in number:
        context["photo" + str(j)] = "/static/out/" + str(photo[i].split("\\")[-1])
        j += 1

    K.clear_session()
    return render(request,"index.html",context)