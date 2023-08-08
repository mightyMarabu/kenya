FROM python:3.10

# maintainer: Sebastian

WORKDIR /app

#RUN apt update && apt install -y unicorn

ADD requirements.txt . 

# install libs
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# add app
COPY . .

CMD ["python3", "main.py", "--host", "0.0.0.0", "--port", "8080"]