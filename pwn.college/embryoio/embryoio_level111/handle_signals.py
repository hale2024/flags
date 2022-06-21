import ast
import signal
import subprocess


pid = int( input("Enter PID of the other process: ") );
signals_str = str( input("Enter list of signals it gave: ") );
signals = list(ast.literal_eval(signals_str));

for sig in signals:
    sig_num = signal.Signals[sig].value;

    subprocess.run(f"kill -{sig_num} {pid}", shell=True);
