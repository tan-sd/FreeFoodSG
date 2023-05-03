FROM python:3-slim
WORKDIR /usr/src/app
COPY  requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./publish_message.py ./
COPY ./amqp_setup.py ./
CMD [ "python", "./publish_message.py" ]