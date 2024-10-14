from flask import Flask, request, render_template, jsonify,redirect,url_for,flash
import subprocess
import os
from datetime import datetime
import ipinfo
from dns_functions.all_records import *
from pw_functions.pw_gen import generate_symbols,generate_random_letters,random_numbers_list,doc_string
from random import shuffle
application = Flask(__name__)
application.secret_key = 'supersecretkey'

@application.route('/')
def index():
    return render_template('index.html')


#################################################
# MAIN PROGRAM FOR IMAPSYNC Email transfer tool #
#################################################


@application.route('/run_imapsync', methods=['POST'])
def run_imapsync():
    # Extracting form data
    imap_source = request.form.get('imap_source')
    user_source = request.form.get('user_source')
    pass_source = request.form.get('pass_source')
    imap_dest = request.form.get('imap_dest')
    user_dest = request.form.get('user_dest')
    pass_dest = request.form.get('pass_dest')
    log_time = datetime.now().strftime('%d-%m-%Y')
    global dir_path
    global filename
    dir_path = '/home/tools/hosting_tools/imapsync-logs'
    filename = f"{user_source}_{user_dest}_{log_time}.log"
    global command
    
    command = (
        f" nice -n18 imapsync"
        f" --host1 {imap_source}"
        f" --user1 {user_source}"
        f" --password1 '{pass_source}'"
        f" --host2 {imap_dest}"
        f" --user2 {user_dest}"
        f" --password2 '{pass_dest}'"
        f" --logdir {dir_path}"
        f" --logfile {filename}"
        f" --addheader"
    )
    
    


    try:
        # Running the command
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8') if result.stdout else "Transfer Completed"
        error = result.stderr.decode('utf-8') if result.stderr else "No Errors"
        return jsonify({'output': output, 'error': error})
    except Exception as e:
        return jsonify({'error': str(e)})



        
########################
# IMAPSYNC FROM FILE ###
########################


ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@application.route('/imapsync_file_method')
def upload_file():
    return render_template('upload.html')

@application.route('/upload', methods=['POST'])
def upload_file_post():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        process_file(file_path)
        flash('File successfully processed.ImapSync Finished')
        return redirect(url_for('upload_file'))
    else:
        flash("File extensions not allowed. Allowed extensions is .txt")
        return  redirect(url_for('upload_file'))

def process_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            h1, u1, p1, h2, u2, p2 = line.split(';')
            now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            log_file = f'imapsync-logs/{u1}_{u2}_{now}.txt'
            imapsync_command = [
                'imapsync',
                '--host1', h1,
                '--user1', u1,
                '--password1', p1,
                '--ssl1',
                '--host2', h2,
                '--user2', u2,
                '--password2', p2,
                '--ssl2'
            ]
            with open(log_file, 'w') as log:
                subprocess.run(imapsync_command, stdout=log, stderr=log)    
    
    
    
    
#################################################
################ DNS PROGRAM SECTION ############
#################################################


def get_full_dns(domain):
    A = get_ip(domain)
    mx= get_mx(domain)
    NS=get_ns(domain)
    txt = get_txt(domain)
    ptr = ptr_lookup(domain)
    
    DNSSEC = whois_info(domain)
    
    return (f"{txt}\n{mx}\n{A}\n{NS}\n{DNSSEC}\n{ptr}")

# The  DNS Check page where you can enter The domain you want to check


@application.route('/dns_check', methods=['POST', 'GET'])
def dns_check():
    if request.method == 'POST':
        domain = request.form['domain']
        return redirect(url_for('domain_dns', domain=domain))
    return render_template('dns.html')


# The DNS check Results page 


@application.route('/domain_dns')
def domain_dns():
    import re
    pattern = r'https://|http://'
    
    domain = request.args.get('domain')
    domain = re.sub(pattern,'',domain).rstrip('/')
    if not domain:
        return "No domain provided", 400
    domain_dns = get_full_dns(domain)
    return render_template('dns_results.html', domain_dns=domain_dns)


##############################
# PASSWORD GENERATOR SECTION #
##############################
                
# Password page route where you can generate your password based on number of 
# symbols , number of digits  , number of letters


@application.route('/password',methods=['GET','POST'])
def password_generator():
    password = ''
    password_list = []
    if request.method == 'POST':
        num_symbols = int(request.form['num_symbols'])
        num_letters = int(request.form['num_letters'])
        num_numbers = int(request.form['num_numbers'])
        
        symbols = ''.join(generate_symbols(num_symbols))
        letters = ''.join(generate_random_letters(num_letters))
        numbs = random_numbers_list(num_numbers)
        password = symbols+letters+numbs
    [password_list.append(p) for p in password ]
    shuffle(password_list)

    return render_template('password.html',password=''.join(password_list))


########################
# IP INFO TOOL SECTION #
########################

# IP INFO PAGE where you can get your own IP and to check another IP's details
# IP Country , Region,City


@application.route('/ip', methods=['POST', 'GET'])
def get_ip_info():
    visitor_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip_info = None

    if request.method == 'POST':
        ip = request.form.get('ip_info')
        ip = ip.strip()
        if ip:
            access_token = 'ipinfo-personal-account-access-token'
            handler = ipinfo.getHandler(access_token)
            details = handler.getDetails(ip)
           
            get_ip_command = f"host {ip} | awk '{{print $5}}'"
            result = subprocess.run(get_ip_command, shell=True, capture_output=True, text=True)
            
            ip_info = {
                "ip": details.ip,
                "hostname" : result.stdout,
                "city" : details.city,
                "region": details.region,
                "country": details.country,
                "org" : details.org,
                # "postal" : details.postal,
                "timezone" : details.timezone,
                "country_name" : details.country_name,
                "loc" : details.loc,
                       
    
  }
           

    return render_template('ip.html', visitor_ip=visitor_ip, ip_info=ip_info)


@application.route('/extra_tools',methods=['POST','GET'])
def check_dkim():
    return render_template('extra_tools.html')



if __name__ == "__main__":
    application.run(host="0.0.0.0",debug=True)
    
