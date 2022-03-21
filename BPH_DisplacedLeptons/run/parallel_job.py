import multiprocessing
import subprocess

def proc(value):
    return subprocess.call('./processor.py %s' % value, shell=True )


pool_obj = multiprocessing.Pool()

answer = pool_obj.map(proc,range(5,15))

