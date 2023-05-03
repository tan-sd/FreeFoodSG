FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./invoke_activity.py ./
COPY ./invokes.py ./
CMD [ "python", "./invoke_activity.py"]