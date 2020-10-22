FROM tensorflow/tensorflow:latest-gpu 
ADD requirements_noTF.txt /
RUN mkdir -p src
ADD dockerTrain.sh /src/
RUN chmod a+x /src/dockerTrain.sh
RUN pip install -r requirements_noTF.txt
CMD [ "./src/dockerTrain.sh" ] 