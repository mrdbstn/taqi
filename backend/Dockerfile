FROM python:3.11

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
COPY . /app/
EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh" ]

