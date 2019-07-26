FROM python:3.7-alpine

WORKDIR /user/src/randology

#ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev python3-dev
# required during runtime.
RUN apk add --no-cache openblas-dev freetype-dev
RUN pip install Cython
RUN pip install numpy
RUN pip install GF2Matrix ripser
COPY . /user/src/randology
RUN python setup.py install
# remove dependancies not required at runtime.
RUN apk del .build-deps

# create directory for data storage and output.
RUN mkdir /user/src/randology/output
ENV OUTPUTDIR /user/src/randology/output/
RUN mkdir /user/src/randology/data
ENV DATADIR /user/src/randology/data/
RUN touch /user/src/randology/config.json
RUn touch /user/src/randology/output/test.txt
CMD ["python", "run_test.py", "config.json"]
