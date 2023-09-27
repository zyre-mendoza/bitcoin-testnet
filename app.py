from flask import Flask, render_template, request
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

app = Flask(__name__)

# Define your Bitcoin Testnet code as a function
def send_bitcoin(sender_private_key, recipient_address, amount_to_send):
    sender_key = PrivateKeyTestnet(sender_private_key)
    tx_hex = sender_key.create_transaction(outputs=[(recipient_address, amount_to_send, 'btc')])
    signed_tx_hex = sender_key.sign_transaction(tx_hex)
    tx_id = NetworkAPI.broadcast_tx_testnet(signed_tx_hex)
    return tx_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender_private_key = request.form['sender_private_key']
        recipient_address = request.form['recipient_address']
        amount_to_send = float(request.form['amount_to_send'])
        
        tx_id = send_bitcoin(sender_private_key, recipient_address, amount_to_send)
        
        return render_template('result.html', tx_id=tx_id)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
