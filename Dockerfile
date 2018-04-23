FROM python:3.6
EXPOSE 8000
RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN pip install -e .
RUN alembic upgrade head
CMD python app.py