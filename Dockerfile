#Identify Python image (I'm using python 13.13.14 so best practice is to use the reduced python image for this version)
FROM python:3.13-slim

#Set the images working directory
WORKDIR /webhook-processsor

#Copy requirements file from the current directory
COPY requirements.txt .

#Install dependencies from the requirements file
RUN python -m pip install --no-cache-dir -r requirements.txt

#Copy the app code into /webhook-processor ex:(/webhook-processor/app)
COPY ./app ./app

#Create a data directory for data.db
RUN mkdir -p /webhook-processor/data

#Expose the API port 
EXPOSE 8000

#Default command when starting the container
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




