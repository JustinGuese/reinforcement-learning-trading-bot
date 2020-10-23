FROM tensorflow/tensorflow:2.1.0
ADD requirements_noTF.txt /
RUN mkdir -p src
ADD . /src/
#ADD dockerTrain.sh /
RUN chmod a+x /src/dockerTrain.sh
RUN pip install -r requirements_noTF.txt
WORKDIR "/src"
RUN ls