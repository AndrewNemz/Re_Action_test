FROM python:3.12-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY Re_Action_test/ /app

WORKDIR /app

CMD ["gunicorn", "Re_Action_test.wsgi:application", "--bind", "0:8000" ]
