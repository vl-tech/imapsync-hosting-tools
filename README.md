# Imapsync/Hosting tools project build with Flask and Waitress
## Tools available
1. Imapsync tool based on the imapsync command and the original project here [imapsync source website](https://imapsync.lamiral.info/)
   - The tool has 2 versions 
   - The first one requires input of user data (source username , password , hostname , and destination username ,hostname and password)
   - The second version is file upload version that reads credentials from a file with the following separation method
   ``` bash
   hostname1;username1;password1;hostname2;username2;password2
   ```
   - Allowed file format is only .txt with `;` separator of the credentials 

2. Hosting tools like Ipinfo [Source Website](https://ipinfo.io/) requires an account at ipinfo.io and the access token
   - The ipinfo token is to be replaced in the tools.py file

3. DNS Checking tools. Checks for DNS configuration of a domain (TXT , MX ,A , DNSSEC , PTR Record types)

4. Mail Records. Embedded tools from [EasyDmarc](easydmarc.com)

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
waitress-serve.exe --listen=0.0.0.0:5000 wsgi:application
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