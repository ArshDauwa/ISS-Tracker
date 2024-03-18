#FROM python:3.9

#RUN mkdir /midterm1-project
#WORKDIR /midterm1-project

#COPY requirements.txt /midterm1-project/requirements.txt
#RUN pip install -r /midterm1-project/requirements.txt

#COPY iss_tracker.py /midterm1-project/iss_tracker.py

#ENTRYPOINT ["python"]
#CMD ["iss_tracker.py"]
#CMD ["test_iss_tracker.py"]


FROM python:3.10

WORKDIR /code

ENV PYTHONPATH=/code
ENV FLASK_APP=iss_tracker.py
ENV FLASK_ENV=development

# Install requirements first to leverage Docker cache
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code

# Expose the port the app runs on
EXPOSE 5001

# Set the default command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
