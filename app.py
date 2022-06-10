from flask import Flask, request, jsonify, render_template
import pandas as pd
import random

app = Flask(__name__,)

@app.route('/')
def index():
    return render_template('chat_bot.html')

counter = False

def send_data(text):
    global counter
    if counter:
        counter = False
        return 'Hello {}. Which stream do you want to choose : (MBBS ,MBA, MS, BE/B.TECH, BSc, LAW). And if you wanna see only: Indian Universities(add - I after stream) , Foreign Universities(add -F after stream) '.format(text)

    greetings = ['hi','hello','hey']
    info = pd.read_csv('data/info.csv')
    info.columns = ['Name','Rank','Address','Special_Code','Website']
    info['Special_Code_1'] = info['Special_Code'].map(lambda x : x.split('-')[0])
    info['Special_Code_1'] = info['Special_Code_1'].map(lambda x : x.replace('/',' '))
    info['all'] = info['Name'] + ' ' + info['Rank'].astype(str) + ' ' + info['Special_Code'] \
                    +' ' + info['Special_Code_1'] +  ' ' + info['Address'] + ' ' + info['Website']
    info['all'] = info['all'].str.lower()
    result = pd.DataFrame()
    for i in text.split():
        if len(i)>0:
            try:
                if i.lower() in greetings:
                    counter = True
                    return random.choice(greetings).title() + '\n What is your name?'


                temp = info[info['all'].str.contains(i.lower())]
                temp = temp[['Name','Address','Website']]
                if len(temp)>0:
                    result = result.append(temp)

                
            except Exception as e:
                print('Error',e)
                pass
    if len(result)>0:
        return result.dropna(how='all')
    else:
        return "No data found"


@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    response_text = send_data(message)
    if isinstance(response_text,pd.DataFrame):
        response_dict = {"df":response_text.to_html(index = False)}
        return jsonify(response_dict)
    else:
        response_dict = {"message":response_text}
    return jsonify(response_dict)

# run Flask app
if __name__ == "__main__":
    app.run()