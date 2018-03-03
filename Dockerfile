# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN  pip install lxml
RUN  pip install prettytable
RUN  pip install requests
RUN  pip install tensorflow 
RUN  pip install imutils

# Make port 80 available to the world outside this container
EXPOSE 443 8888 6006 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "trade_app.py"]
