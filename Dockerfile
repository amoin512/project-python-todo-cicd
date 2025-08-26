FROM python:3.9-slim
WORKDIR /home-app
COPY code.py /home-app
CMD [ "python", "code.py" ]