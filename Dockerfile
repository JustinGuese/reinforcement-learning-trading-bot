FROM tensorflow/tensorflow:latest-gpu 
ADD requirements_noTF.txt /
RUN mkdir -p src
#ADD dockerTrain.sh /
#RUN chmod a+x ./dockerTrain.sh
RUN pip install -r requirements_noTF.txt
RUN chmod a+x ./src/dockerTrain.sh
RUN ls 
CMD [ "./src/dockerTrain.sh" ] 