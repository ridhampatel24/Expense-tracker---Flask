FROM python:3.9-slim
WORKDIR /expense_tracker
COPY requirement.txt /expense_tracker/
RUN pip install -r requirement.txt
COPY . /expense_tracker/
EXPOSE 5000
CMD [ "python3", "server.py" ]