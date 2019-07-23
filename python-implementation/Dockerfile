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

#CMD ["python", "setup.py", "install"]
RUN apk del .build-deps
CMD ["python", "run_test.py"]
