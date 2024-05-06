FROM python:3.9-slim
WORKDIR /expense_tracker
COPY requirement.txt /expense_tracker/
RUN apt-get update -y
RUN apt-get install pkg-config -y
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
RUN  pip install --upgrade pip
RUN pip install -r requirement.txt
COPY . /expense_tracker/
EXPOSE 5000
CMD [ "python3", "server.py" ]