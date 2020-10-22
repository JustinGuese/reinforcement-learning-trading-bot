FROM tensorflow/tensorflow:latest-gpu 
ADD requirements_noTF.txt /
RUN mkdir -p src
ADD dockerTrain.sh /
RUN chmod a+x ./dockerTrain.sh
RUN pip install -r requirements_noTF.txt
CMD [ "/src/dockerTrain.sh" ] 