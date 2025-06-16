#python version to use in container
FROM python:3.10.12

#Work directory in container
WORKDIR /app

#Copy local to container
COPY . /app

#requirements library
COPY requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

#command to execute container is running
CMD ["python3", "main.py"]