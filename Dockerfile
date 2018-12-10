FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN apt update && apt install cron -y && \
    echo '0 * * * * /usr/local/bin/python3.7 /code/quotation/scripts/get_currency_data.py >> /var/log/mycron.log 2>&1' >> mycron && \
    crontab mycron && rm -rf mycron
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
ENTRYPOINT env >> /etc/environment && service cron start && python3 manage.py runserver 0.0.0.0:8000