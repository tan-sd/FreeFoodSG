FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./forum_info.py  ./
CMD ["python", "./forum_info.py" ]

# FROM mysql:latest
# ENV DB_HOST=localhost
# ENV DB_PORT=3306
# ENV DB_NAME=mydb
# ENV DB_USER=user
# ENV DB_PASSWORD=password
# COPY ./forum_db.sql /docker-entrypoint-initdb.d/

# EXPOSE 3306