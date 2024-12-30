# Imapsync/Hosting tools project build with Python Flask and Waitress

## Tools available

1. Imapsync tool based on the imapsync command and the original project here [imapsync source website]

(<https://imapsync.lamiral.info/>)

- The tool has 2 versions

- The first one requires input of user data (source username , password , hostname , and destination username ,hostname and password)

- The second version is file upload version that reads credentials from a file with the following separation method

   ``` bash
   hostname1;username1;password1;hostname2;username2;password2
   ```

- Allowed file format is only .txt with `;` separator of the credentials

2.Hosting tools like Ipinfo [Source Website](https://ipinfo.io/) requires an account at ipinfo.io and the access token

- The ipinfo token is to be replaced in the tools.py file

3.DNS Checking tools. Checks for DNS configuration of a domain (TXT , MX ,A , DNSSEC , PTR Record types)

4.Mail Records. Embedded tools from [EasyDmarc](easydmarc.com)

## Installation of the imapsync command on different distributions

- [INSTALLATION GUIDES PAGE](https://imapsync.lamiral.info/#install)

## Bulding the tool

1. Clone the Repo with git clone
2. Make sure you have Python with version higher than 3.10
3. Install globally the venv module or virtualenv package
   - `dnf -y install python3-virtualenv`
   - `dnf -y install python-virtualenv`
   - `apt-get install virtualenv -y`
4. Create virtualenvironment folder with `virtualenv .venv`
5. Activate the virtualenvironment `source .venv/bin/activate`
6. Install the packages.txt file with the python dependencies
   - `pip3 install -r packages.txt`

## Test the application before setting it up as a service

```ruby
waitress-serve --listen=0.0.0.0:5000 wsgi:application
```

- You will be able to access the app on port 5000 with your local IP such as 192.168.1.15:5000 for example

- Once this is done you can set it up as a service by copying the service file
  - Copy the file to /etc/systemd/system/tools.service
  - Enable the service systemctl enable --now tools.service

## Running the service

- You can run it as a regular user (recommended) or as root
- The App is build for personal usage and internal usage
- It has no security policies implemented into the form-post requests

## Create user called tools

```bash
useradd -m tools -s /sbin/nologin

```

- Create it without a login but with a home so you can locate the files there
- Make sure all files have permissions to be run as user tools
- `chown -R /home/tools/`

## Linux Dependencies for the DNS checks

- Make sure to install bind-utils
- `dnf -y install bind-utils`
- `apt install -y bind9-utils`

## Configuring the IpInfo tool in file tools.Python

- On line 229 in the code replace the token with your personal account token from ipinfo official website.
- The free api token has 50 000 requests per month.
- Here is the actual code where you have to replace it with your token

```pythons
 access_token = 'ipinfo-personal-account-access-token'
 handler = ipinfo.getHandler(access_token)
```

## Docker version

### Files Needed for the docker image

1. Dockerfile
2. imapsync requirements file. You can find the apt install dependency command here as well [Imapsync Install guide](https://imapsync.lamiral.info/INSTALL.d/INSTALL.Debian.txt)

- Filename *install-requirements-imapsync.sh* uploaded in the repo

- Dockerfile

```bash
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
```

- Build the image with *docker build .* at the location of the Dockerfile and all files in folder *imapsync-hosting-tools*

- Then just run the container with *docker run -d -p 8000:8000 <Docker-Image-ID>* if you
- To check the list of docker images use `docker image ls` and obtain the id from there

## Firewall setup

- For firewalld use the bellow command.

```bash
firewall-cmd --permanent --add-port=8000/tcp&&firewall-cmd --reload

```

- If you are using ufw

```bash
ufw allow 8000&&ufw reload
```

## Tool Screenshots

### DNS Check Tool

![DNS Check Tool](https://drive.google.com/file/d/1Hna8y8EextFy24au4FS8_DXKhYQg6mKD/view?usp=sharing)

### Imapsync From File Tool

![Imapsync From File Tool](https://drive.google.com/file/d/1ifvXGXiZfv4xteBLNmiy15Kd9QcAQquC/view?usp=drive_link)

### Imapsync Tool

![Imapsync Tool](https://drive.google.com/file/d/1IK1iQOdkfLI77PJUXsNYtgnLaHeeApGG/view?usp=drive_link)

### Ip check/Ipinfo tool

![Ip check/Ipinfo tool](https://drive.google.com/file/d/15hDaKAinagT-3gRvKb9O3O-VmlL-nVR6/view?usp=drive_link)

### Pass generator tool

![Pass generator tool](https://drive.google.com/file/d/1yBmTDi04fLEMU-BcPJFDJCe045A6lFiB/view?usp=drive_link)

### Easy Dmarc Embedded Tools

![Easy Dmarc Embedded Tools](https://drive.google.com/file/d/1BVoaPhGkBKnJZprMWc3EUdrvX38auhu1/view?usp=drive_link)
