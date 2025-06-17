#python version to use in container
FROM python:3.10.12

RUN apt-get update && apt-get install -y nano

RUN apt-get install -y sqlite3 

#Work directory in container
WORKDIR /app

#Copy local to container
COPY . /app

#requirements library
RUN pip install --no-cache-dir -r requirements.txt

#command to execute container is running
CMD ["python3", "main.py"]