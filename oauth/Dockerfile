FROM python:3.11-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
# ADD：將檔案加到 images 內
ADD . /app

# Install the dependencies
# build 時使用，會執行此命令
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# run the command to start uWSGI
# run container 時要執行的命令
CMD ["uwsgi", "--ini", "uwsgi.ini"]
