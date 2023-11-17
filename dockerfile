FROM python:3.8
WORKDIR .
COPY . ./
RUN pip install -r requirements.txt
RUN mkdir -p /usr/src/modules/logs
CMD ["python3", "rest_api.py", "--host", "0.0.0.0", "--port", "5050"]