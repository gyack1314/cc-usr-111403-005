"""查询批包的JSON行编码，仅负责格式和身份。"""
import json
from .storage import encode

def pack(message):
    validate(message);return encode(message)+b'\n'
def unpack(raw):
    if not raw.endswith(b'\n') or b'\n' in raw[:-1]:raise ValueError('包边界非法')
    message=json.loads(raw);validate(message);return message
def validate(message):
    for k in ('query_id','execution_id','call_id','row_ids','registry_digest'):
        if k not in message:raise ValueError('批包身份缺失')
    if type(message['execution_id']) is not int or message['execution_id']<0:raise ValueError('执行代非法')
    if not isinstance(message['row_ids'],list) or len(set(message['row_ids']))!=len(message['row_ids']):raise ValueError('行身份重复')
