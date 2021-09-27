FROM python:3.9
EXPOSE 8000
WORKDIR /usr/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy sourcecode and compiled frontend
COPY . .

ENTRYPOINT ["/usr/src/entrypoint.sh"]
CMD ["gunicorn", "leaderboard.wsgi:application", "--bind", "0.0.0.0:8000"]
