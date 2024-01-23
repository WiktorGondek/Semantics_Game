
FROM python:3.10

COPY ./ /Semantics_Game/

WORKDIR /Semantics_Game/

RUN pip install -r requirements.txt

RUN pip install uwsgi

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--master", "-p", "2", "-w", "flask_semantics:create_app"]
