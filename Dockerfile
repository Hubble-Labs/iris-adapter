FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
