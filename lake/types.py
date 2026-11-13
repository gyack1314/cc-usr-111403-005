"""扩展函数参数与回包值的确定类型检查。"""
def check_value(value,typ):
    if value is None:
        if typ.get('nullable',False):return
        raise ValueError('必选值为空')
    kind=typ['kind']
    valid=(kind=='int64' and type(value) is int and -(2**63)<=value<2**63) or (kind=='bool' and type(value) is bool) or (kind=='string' and type(value) is str)
    if not valid:raise ValueError('函数值类型不符')

def check_columns(columns,types,row_ids):
    if len(columns)!=len(types) or len(set(row_ids))!=len(row_ids):raise ValueError('批参数身份或宽度非法')
    for col,typ in zip(columns,types):
        if len(col)!=len(row_ids):raise ValueError('批参数长度不符')
        for value in col:check_value(value,typ)
