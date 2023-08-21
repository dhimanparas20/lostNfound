# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that the Flask development server will listen on
EXPOSE 5000

# Define the command to run your application using the Flask development server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
