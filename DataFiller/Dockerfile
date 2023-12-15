FROM python:3.9

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install 'pydantic[email]'

COPY . ./
CMD [ "python", "./main.py"]
