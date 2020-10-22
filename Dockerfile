FROM tensorflow/tensorflow:latest-gpu 
ADD requirements_noTF.txt /
RUN pip install -r requirements_noTF.txt