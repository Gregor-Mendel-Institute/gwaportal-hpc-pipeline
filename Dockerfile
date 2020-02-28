FROM python:3
RUN useradd --uid=10372 -ms /bin/bash gwaportal
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /tmp
RUN pip install --no-cache-dir /tmp && rm -fr /tmp/*
USER gwaportal
ENTRYPOINT ["celery", "worker", "--app=gwaportal_hpc_pipeline", "--loglevel=INFO", "--concurrency=2", "-n gwaportal-worker@%h", "--time-limit=300"]