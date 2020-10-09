$ adb shell perfetto \
  -c - --txt \
  -d \
  -o /data/misc/perfetto-traces/trace \
<<EOF

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
flush_period_ms: 10000

EOF
