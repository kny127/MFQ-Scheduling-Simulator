import sys
from collections import deque

current_time = 0
current_que = None
finished = 0

process_info = {}
Q0 = deque()
Q1 = deque()
Q2 = []
q2_current_pid = None

timeline = []

def make_structure(filename="input.txt"):
    global process_info, Q0, Q1, Q2, q2_current_pid, timeline, finished
    process_info.clear()
    Q0.clear()
    Q1.clear()
    Q2.clear()
    timeline.clear()
    finished = 0
    q2_current_pid = None

    with open(filename, "r") as f:
        lines = f.readlines()
    lines = [line for line in lines if line.strip() != ""]

    n = int(lines[0].strip())

    for i in range(1, n+1):
        pid, at, bt = map(int, lines[i].split())
        process_info[pid] = {
            'AT': at,
            'BT': bt,
            'remain_BT': bt,
            'completion_time': None,
            'TT': 0,
            'WT': 0,
            'quantum_run': 0
        }

def new_arrival():
    global current_time, process_info, Q0
    for pid in sorted(process_info.keys()):
        info = process_info[pid]
        if (info['AT'] == current_time and
            info['completion_time'] is None and
            info['remain_BT'] == info['BT']):
            Q0.append(pid)

def check_preempt():
    global current_que, Q0, Q1
    if current_que is None:
        return 0
    elif current_que == 1:
        if len(Q0) > 0:
            return 0
    elif current_que == 2:
        if len(Q0) > 0:
            return 0
        elif len(Q1) > 0:
            return 1
    return 3

# Q0: RR, time quantum = 2
def run_q0():
    global Q0, Q1, finished, current_time, process_info
    if len(Q0) == 0:
        return None
    pid = Q0[0]

    process_info[pid]['remain_BT'] -= 1
    process_info[pid]['quantum_run'] += 1

    if process_info[pid]['remain_BT'] == 0:
        process_info[pid]['completion_time'] = current_time + 1
        finished += 1
        Q0.popleft()
        process_info[pid]['quantum_run'] = 0
        return pid
    else:
        if process_info[pid]['quantum_run'] >= 2:
            Q0.popleft()
            process_info[pid]['quantum_run'] = 0
            Q1.append(pid)
        return pid

# Q1: RR, time quantum = 4
def run_q1():
    global Q1, Q2, finished, current_time, process_info
    if len(Q1) == 0:
        return None
    pid = Q1[0]
    process_info[pid]['remain_BT'] -= 1
    process_info[pid]['quantum_run'] += 1

    if process_info[pid]['remain_BT'] == 0:
        process_info[pid]['completion_time'] = current_time + 1
        finished += 1
        Q1.popleft()
        process_info[pid]['quantum_run'] = 0
        return pid
    else:
        if process_info[pid]['quantum_run'] >= 4:
            Q1.popleft()
            process_info[pid]['quantum_run'] = 0
            Q2.append(pid)
        return pid

def run_q2():
    global Q2, q2_current_pid, finished, current_time, process_info
    if q2_current_pid is None:
        if len(Q2) == 0:
            return None
        # SPN
        Q2.sort(key=lambda x: (process_info[x]['remain_BT'], x))
        pid = Q2.pop(0)
        q2_current_pid = pid
    else:
        pid = q2_current_pid
    process_info[pid]['remain_BT'] -= 1

    if process_info[pid]['remain_BT'] == 0:
        process_info[pid]['completion_time'] = current_time + 1
        finished += 1
        q2_current_pid = None
        return pid
    else:
        return pid

def merge_timeline(timeline):
    if not timeline:
        return []
    merged = []
    prev = timeline[0]
    for rec in timeline[1:]:
        if rec[3] == prev[3] and rec[0] == prev[1]:
            prev = (prev[0], rec[1], prev[2], prev[3])
        else:
            merged.append(prev)
            prev = rec
    merged.append(prev)
    return merged


def MFQ_scheduling(filename="input.txt"):
    global current_time, current_que, finished, timeline
    global process_info, Q0, Q1, Q2, q2_current_pid

    make_structure(filename)
    total_process = len(process_info)
    current_time = 0
    current_que = None
    finished = 0

    while finished < total_process:
        new_arrival()

        if current_que is None:
            if len(Q0) > 0:
                current_que = 0
            elif len(Q1) > 0:
                current_que = 1
            elif len(Q2) > 0:
                current_que = 2

        result = check_preempt()
        if result != 3:
            current_que = result

        executed_pid = None
        if current_que == 0:
            executed_pid = run_q0()
        elif current_que == 1:
            executed_pid = run_q1()
        elif current_que == 2:
            executed_pid = run_q2()

        if executed_pid is None:
            timeline.append((current_time, current_time + 1, "0", 0))
        else:
            timeline.append((current_time, current_time + 1, "Q" + str(current_que), executed_pid))

        current_time += 1
        if current_que == 0 and len(Q0) == 0:
            current_que = None
        elif current_que == 1 and len(Q1) == 0:
            current_que = None
        elif current_que == 2 and len(Q2) == 0 and q2_current_pid is None:
            current_que = None

    print_results()

def print_results():
    global process_info, timeline

    for pid, info in process_info.items():
        info['TT'] = info['completion_time'] - info['AT']
        info['WT'] = info['TT'] - info['BT']

    merged_timeline = merge_timeline(timeline)

    print("\n=== Gantt Chart ===")
    chart = ""
    for seg in merged_timeline:
        duration = seg[1] - seg[0]
        dashes = "-" * duration
        if seg[3] == 0:
            chart += f"[-0({duration}){dashes}]"
        else:
            chart += f"[-P{seg[3]}({duration}){dashes}]"
    print(chart)

    print("\n=== 각 프로세스 TT, WT ===")
    sum_tt = sum_wt = 0
    for pid in sorted(process_info.keys()):
        tt = process_info[pid]['TT']
        wt = process_info[pid]['WT']
        sum_tt += tt
        sum_wt += wt
        print(f"P{pid} => TT={tt}, WT={wt}")

    n = len(process_info)
    print(f"\nAverage TT = {sum_tt/n:.2f}, Average WT = {sum_wt/n:.2f}")

def create_input_txt(content):
    with open("input.txt", "w") as f:
        f.write(content)

ex_1 = """
3
1 0 2
2 0 2
3 5 3
"""
create_input_txt(ex_1)
print("========= Case 1 ========")
MFQ_scheduling("input.txt")
print()

ex_2 = """
5
1 0 10
2 1 10
3 3 2
4 6 3
5 7 4
"""
create_input_txt(ex_2)
print("========= Case 2 ========")
MFQ_scheduling("input.txt")
print()

ex_3 = """
7
1 0 10
2 3 2
3 4 1
4 7 6
5 8 2
6 9 1
7 10 3
"""
create_input_txt(ex_3)
print("========= Case 3 ========")
MFQ_scheduling("input.txt")
print()

