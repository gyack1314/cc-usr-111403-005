"""内部已登记函数及其版本声明。"""
import os,time
from .storage import digest

def double(values):return [None if v is None else 2*v for v in values]
_count=0
def stateful(values):
    global _count
    _count+=1;return [_count for _ in values]
def explode(values):raise ValueError('编码映射不可用')
def abort(values):os._exit(17)
def stall(values):time.sleep(60);return values

REGISTRY={name:{'id':name,'version':'1','callable':name,'input_types':[{'kind':'int64','nullable':True}],'output_type':{'kind':'int64','nullable':True},'pure':name=='double','isolation_domain':'team-A'} for name in ('double','stateful','explode','abort','stall')}

def registry_digest():return digest(REGISTRY)
def local_call(name,columns):return globals()[REGISTRY[name]['callable']](*columns)
