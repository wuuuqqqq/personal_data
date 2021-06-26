import datetime

import telegram, json, logging
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.secret_key = 'lAlAlA123'
basic_auth = BasicAuth(app)

# Yes need to have -, change it!
chatID = "-xchatIDx"

# Authentication conf, change it!
app.config['BASIC_AUTH_FORCE'] = False
app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'

# Bot token, change it!
bot = telegram.Bot(token="1318464227:AAENlGLjYALQTONxCI7b8UTevbrLhp_aqwo")


@app.route('/alert', methods=['POST'])
def postAlertmanager():

    try:
        content = json.loads(request.get_data())
        print(content)
        for alert in content['alerts']:
            message = "状态情况: "+alert['status']+"\n"
            if 'name' in alert['labels']:
                message += "故障主机："+alert['labels']['instance']+"("+alert['labels']['name']+")\n"
            else:
                message += "故障主机："+alert['labels']['instance']+"\n"
            if 'info' in alert['annotations']:
                message += "Info: "+alert['annotations']['info']+"\n"
            if 'summary' in alert['annotations']:
                message += "故障标题："+alert['annotations']['summary']+"\n"
            if 'description' in alert['annotations']:
                message += "故障事件："+alert['annotations']['description']+"\n"
            if alert['status'] == "resolved":
                correctDate = (parser.parse(alert['endsAt'])+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                message += "恢复时间："+correctDate
            elif alert['status'] == "firing":
                correctDate = (parser.parse(alert['startsAt'])+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                message += "故障时间："+correctDate
            bot.sendMessage(chat_id="-329781952", text=message)
            return "Alert OK", 200
    except Exception as error:
        bot.sendMessage(chat_id="-329781952", text="Error to read json: "+str(error))
        app.logger.info("\t%s", error)
        return "Alert fail", 200


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=9119)

