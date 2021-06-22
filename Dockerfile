FROM python:3.9

WORKDIR /app

# copy repo contents
COPY setup.py README.md ./
COPY necroptimade ./necroptimade
RUN pip install -e .

ARG PORT=8000
EXPOSE ${PORT}

COPY run.sh ./

CMD ["/app/run.sh"]
