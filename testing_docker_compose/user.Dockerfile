FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ../
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./user_info.py  ./
CMD [ "python", "./user_info.py" ]

FROM mysql:latest
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_NAME=mydb
ENV DB_USER=user
ENV DB_PASSWORD=password
COPY ./user_info.sql /docker-entrypoint-initdb.d/
