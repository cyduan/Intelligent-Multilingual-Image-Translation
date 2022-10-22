import requests
import json
import re
def translate(text, from_lang, to_lang):
    # 代换掉文本中的一些特殊符号，方便转译
    text = text.replace("\\", "\\\\\\\\")
    text = text.replace("\"", "\\\\\\\"")
    text = text.replace("\n", "\\\\n")
    text = text.replace("\r", "\\\\r")
    # 请求地址
    data ={
        "f.req":"""[[["MkEWBc","[[\\"%s\\",\\"%s\\",\\"%s\\",true],[null]]",null,"generic"]]]""" % (text, from_lang, to_lang)
    }
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"}
    result = requests.post("https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&source-path=%2F&f.sid=8445046605529310777&bl=boq_translate-webserver_20220817.10_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=230230&rt=c", data = data)
    match = re.search("(\\[\\[\"wrb.fr\".*?\"\\]\\])\\n\\d+", result.text, flags = 0)
    resulttext = ""
    if match:
        jsoncode = json.loads(match.group(1))
        transate = json.loads(jsoncode[0][2])
        for i in range(len(transate[1][0][0][5])):
            resulttext = resulttext + transate[1][0][0][5][i][0]
    return resulttext
