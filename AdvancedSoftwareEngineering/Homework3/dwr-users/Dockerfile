FROM python:3.7-alpine
ADD . /UsersService
WORKDIR /UsersService
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]