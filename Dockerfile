FROM tensorflow/tensorflow:latest-gpu 
ADD requirements_noTF.txt /
RUN mkdir -p src
ADD . /src/
#ADD dockerTrain.sh /
RUN chmod a+x /src/dockerTrain.sh
RUN pip install -r requirements_noTF.txt
RUN ls /src
RUN cd src
CMD [ "./dockerTrain.sh" ] 