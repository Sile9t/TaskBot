FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir instance

COPY . .

CMD ["/bin/bash", "-c", "alembic upgrade head & python main.py"]