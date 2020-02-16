FROM python:3.7-alpine
ADD . /StoriesService
WORKDIR /StoriesService
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]