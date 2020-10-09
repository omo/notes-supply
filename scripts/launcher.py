"""Launcher: Launch an app and collect some data.
"""

from __future__ import annotations

import icws
import time
import sys

_DEFAULT_PERFETTO_CONFIG = """
buffers: {
    size_kb: 129024
    fill_policy: RING_BUFFER
}
buffers: {
    size_kb: 2048
    fill_policy: RING_BUFFER
}
data_sources: {
    config {
        name: "linux.process_stats"
        target_buffer: 1
        process_stats_config {
            scan_all_processes_on_start: true
        }
    }
}
data_sources: {
    config {
        name: "linux.ftrace"
        ftrace_config {
            ftrace_events: "sched/sched_switch"
            ftrace_events: "power/suspend_resume"
            ftrace_events: "sched/sched_wakeup"
            ftrace_events: "sched/sched_wakeup_new"
            ftrace_events: "sched/sched_waking"
            ftrace_events: "power/cpu_frequency"
            ftrace_events: "power/cpu_idle"
#            ftrace_events: "raw_syscalls/sys_enter"
#            ftrace_events: "raw_syscalls/sys_exit"
            ftrace_events: "sched/sched_process_exit"
            ftrace_events: "sched/sched_process_free"
            ftrace_events: "task/task_newtask"
            ftrace_events: "task/task_rename"
            ftrace_events: "lowmemorykiller/lowmemory_kill"
            ftrace_events: "oom/oom_score_adj_update"
            ftrace_events: "ftrace/print"
            atrace_categories: "gfx"
            atrace_categories: "input"
            atrace_categories: "view"
            atrace_categories: "wm"
            atrace_categories: "am"
            atrace_categories: "camera"
            atrace_categories: "hal"
            atrace_categories: "res"
            atrace_categories: "dalvik"
            atrace_categories: "bionic"
            atrace_categories: "pm"
            atrace_categories: "ss"
            atrace_categories: "aidl"
            atrace_categories: "nnapi"
            atrace_categories: "binder_driver"
            atrace_apps: "*"
        }
    }
}
#duration_ms: 10000
flush_period_ms: 10000
"""

class Perfetto(object):
    """A 'perfetto' CLI wrapper."""
    def __init__(self, filename: str, config: str = _DEFAULT_PERFETTO_CONFIG):
        self.filename = filename
        self.filename_nogz = filename.replace('.gz', '')
        self.config = config
        pass
    
    def start(self) -> Perfetto: 
        icws.adb(
"""shell perfetto -c - --txt -d -o /data/misc/perfetto-traces/trace <<EOF
{}
EOF
""".format(self.config))
        return self

    def _wait_til_settle_size(self, filename):
        def check(sleep):
            time.sleep(sleep)
            return icws.ascall('ls -l ' + filename)
        while check(0) != check(1):
            pass
        

    def stop(self):
        icws.ashell('pkill perfetto')
        self._wait_til_settle_size('/data/misc/perfetto-traces/trace')
        icws.adb('pull /data/misc/perfetto-traces/trace {}'.format(self.filename_nogz))
        if self.filename != self.filename_nogz:
            icws.shell('gzip {}'.format(self.filename_nogz))

    def __enter__(self):
        return self.start()

    def __exit__(self ,type, value, traceback):
        return self.stop()


def _sleep_with_dots(sleep):
    left = sleep
    while left > 0:
        time.sleep(1)
        sys.stdout.write('.')
        sys.stdout.flush()
        left -= 1
    sys.stdout.write('\n')
    sys.stdout.flush()

def trace_fresh_launch(app: str, filename: str, config: str = _DEFAULT_PERFETTO_CONFIG, sleep: int = 5):
    with Perfetto(filename, config):
        icws.launch_fresh(app)
        _sleep_with_dots(sleep)


if __name__ == '__main__':
    app = sys.argv[1]
    tag = sys.argv[2]
    icws.adb('root')
    icws.adb('wait-for-device')
    filename = icws.timestamp_fingerprint() + '_' + tag + '.pftrace.gz'
    trace_fresh_launch(app, filename)
