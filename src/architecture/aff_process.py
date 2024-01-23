import sys

ARGS = sys.argv[1:]

lenmax = max([ len(proc) for proc in ARGS ])

def aff_proc(proc_name):
    print('╭─'+'─'*lenmax + '─╮')
    print('│ '+ proc_name.center(lenmax) + ' │')
    print('╰─'+'─'*lenmax + '─╯')


for proc in ARGS : aff_proc(proc)
