FROM python:3-slim
WORKDIR /usr/src/app
COPY  requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./manage_food.py ./
COPY ./invokes.py ./
COPY ./invoke_activity.py ./
CMD [ "python", "./manage_food.py" ]
