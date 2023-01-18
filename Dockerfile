FROM python:latest
EXPOSE 5000
COPY ./ /app
WORKDIR /app
RUN apt-get update \
    && apt-get install -y default-mysql-client
RUN pip install -r requirements.txt
CMD [ "python3", "init.py"]