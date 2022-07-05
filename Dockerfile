FROM python:3.10-slim

ENV HOME /code
WORKDIR $HOME
COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt
COPY . .

#CMD flask run -h 0.0.0.0 -p 80
RUN export FLASK_APP='run.py'
RUN export FLASK_ENV='development'

CMD ["sh", "start_app.sh"]