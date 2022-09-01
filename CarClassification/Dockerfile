FROM python:3.6

run mkdir /mp12

COPY requirements.txt /mp12
WORKDIR /mp12
RUN pip install --no-cache-dir -r requirements.txt

COPY classify.py /mp12

ENV DATASET=mnist
ENV TYPE=cnn

CMD ["python", "/mp12/classify.py"]
