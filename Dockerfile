FROM python:2.7
RUN mkdir -p /usr/src/ytenx
WORKDIR /usr/src/ytenx
ADD requirements.txt /usr/src/ytenx
RUN pip install -v -r requirements.txt
COPY . /usr/src/ytenx
EXPOSE 8000
CMD ["gunicorn", "ytenx.wsgi", "-b", "0.0.0.0:8000"]
