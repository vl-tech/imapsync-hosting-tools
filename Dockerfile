# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /imapsync-hosting-tools

# Copy the current directory contents into the container at /app
COPY . /imapsync-hosting-tools

# Copy requirements.txt file
COPY requirements.txt /imapsync-hosting-tools/requirements.txt
COPY install-requirements-bash.sh /imapsync-hosting-tools
# Install dependencies from requirements.txt and bash
RUN apt-get update && apt-get install -y bash && \
    bash -c "apt-get install -y python3.11 python3.11-venv python3.11-dev wget"
RUN bash -c "pip3 install --upgrade pip"
RUN bash -c "pip3 install --no-cache-dir -r requirements.txt"
RUN bash -c "wget -N https://imapsync.lamiral.info/imapsync"
RUN chmod +x imapsync
RUN cp imapsync /usr/local/bin/imapsync
RUN bash install-requirements-bash.sh
# Expose port 8000 for the Hosting tools server
EXPOSE 8000

# Define the command to run Hosting Tools on container start
CMD ["python3.11", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]