FROM python:3-slim
WORKDIR /usr/src/app
COPY  requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./send_email_forum.py ./
COPY ./amqp_setup.py ./
COPY ./credentials.json ./
CMD [ "python", "./send_email_forum.py" ]