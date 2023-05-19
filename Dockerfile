FROM python:3.11

ENV HOST=0.0.0.0
ENV PORT=8000

ENV TOKENS_LIFETIME=604800
ENV SALT=553e24d57992f249aa98c5a55c4f28fc

COPY ./ /app/

WORKDIR /app

RUN apt update
RUN apt install ffmpeg -y
RUN pip3 install -r requirements.txt

ENTRYPOINT python3.11 -u main.py