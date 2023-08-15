FROM python:3.11

RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/

RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 8000

COPY ./bot_entrypoint.sh /app/entrypoint.sh
COPY ./.env /app/.env
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "backend/manage.py", "runbot"]
