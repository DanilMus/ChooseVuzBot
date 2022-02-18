FROM python:3.7-alpine3.14

COPY bot.py /
COPY app/* app/
COPY app/handlers/* app/handlers/
COPY app/criteria_async/* app/criteria_async/
COPY config/* config/
#COPY data/* data/

RUN mkdir -p /data
RUN pip install --no-cache-dir aiogram
RUN pip install --no-cache-dir beautifulsoup4
RUN pip install --no-cache-dir lxml
#RUN pip install --no-cache-dir app

CMD [ "python", "/bot.py" ]
