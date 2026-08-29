content = '''# CPU Scheduling Algorithms

## Why Scheduling Matters

The CPU scheduler decides which process in the ready queue gets the CPU next. Good scheduling improves CPU utilization, throughput, and fairness while minimizing waiting time and turnaround time. Different algorithms make different tradeoffs between these goals, and the right choice depends heavily on whether the system is optimizing for batch processing, interactive use, or real-time constraints.

## First Come First Serve (FCFS)

Processes are executed in the order they arrive in the ready queue, using a simple FIFO structure. It is easy to implement and understand, but it has a major drawback known as the convoy effect, where a long process at the front of the queue causes all shorter processes behind it to wait an unfairly long time, significantly increasing the average waiting time across all processes.

## Shortest Job First (SJF)

The process with the smallest execution time is scheduled next. In non-preemptive SJF, once a process starts running it continues until completion. In preemptive SJF, also called Shortest Remaining Time First, a newly arrived process with a shorter remaining time can interrupt the currently running process. SJF is provably optimal for minimizing average waiting time, but it requires knowing each process's execution time in advance, which is rarely possible in real systems and is usually estimated using the exponential average of past CPU bursts.

## Round Robin (RR)

Each process gets a fixed time slice called a quantum. If a process doesn't finish within its quantum, it is preempted and moved to the back of the ready queue.

CODEBLOCK_PLACEHOLDER

Choosing the right quantum size is critical: too small a quantum causes excessive context-switching overhead relative to actual work done, while too large a quantum makes Round Robin behave almost identically to FCFS, losing its fairness benefits.

## Priority Scheduling

Each process is assigned a priority value, and the highest priority process in the ready queue runs first. The major risk with this approach is starvation, where low priority processes may never get executed if a steady stream of higher priority processes keeps arriving. This is commonly solved using aging, a technique where a waiting process's priority is gradually increased the longer it stays in the ready queue, eventually guaranteeing it will run.
'''

code_block = chr(96)*3 + "\nTime Quantum = 4ms\nProcess | Burst Time\nP1      | 10\nP2      | 5\nP3      | 8\n\nExecution order: P1(4) P2(4) P3(4) P1(4) P2(1) P3(4) P1(2)\n" + chr(96)*3

content = content.replace("CODEBLOCK_PLACEHOLDER", code_block)

with open("data/docs/os_scheduling.md", "w", encoding="utf-8") as f:
    f.write(content)

print("File written successfully")
print("Length:", len(content))