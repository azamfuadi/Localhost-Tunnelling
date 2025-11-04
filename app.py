from flask import Flask, redirect, url_for, request, render_template, jsonify

from flaredantic import FlareTunnel, FlareConfig
from pathlib import Path
import threading

app = Flask(__name__)

public_url = ''

@app.route('/dashboard/<name>')
def dashboard(name):
   return 'welcome %s' % name

@app.route('/publiclocalhost')
def publiclocalhost():
   global public_url
   return jsonify({'public_url': public_url})

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('dashboard',name = user))
   else:
      user = request.args.get('name')
      return render_template('login.html')
      
   
def run_tunnel():
   port = 8080
   global public_url
   cloudflare_config = FlareConfig(
      port=port, 
      bin_dir=Path.home()/".my-tunnnels",
      timeout=60, 
      verbose=True
   )
   with FlareTunnel(cloudflare_config) as tunnel:
      print(f"http://localhost:{port} available at: {tunnel.tunnel_url}")
      public_url = tunnel.tunnel_url
      app.run(host='0.0.0.0', port='5000')

if __name__ == '__main__':
   threading.Thread(target=run_tunnel).start()
