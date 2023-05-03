FROM python:3-slim
WORKDIR /usr/src/app
COPY  requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./manage_forum.py ./invokes.py ./invoke_activity.py ./amqp_setup.py ./
CMD [ "python", "./manage_forum.py" ]