FROM tensorflow/tensorflow:latest-gpu 
ADD requirements_noTF.txt /
RUN pip install -f requirements_noTF.txt