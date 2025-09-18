# 1. Start with a base image that has Python installed
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
#    (You need to create a requirements.txt file first!)
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application's source code into the container
COPY . .

# 6. Expose the port that your Flask app runs on
EXPOSE 5000

# 7. Define the command to run your application
#    --host=0.0.0.0 is crucial to make it accessible from outside the container
CMD ["flask", "run", "--host=0.0.0.0"]