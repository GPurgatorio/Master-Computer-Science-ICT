FROM python:3.7-alpine
ADD . /dice_service
WORKDIR /dice_service
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]
