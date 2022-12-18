'''解码'''

import sys

def split_ms(pb_instance, ms):
    jobs = []
    current = 0

    for index, job in enumerate(pb_instance['jobs']):
        jobs.append(ms[current:current+len(job)])
        current += len(job)

    return jobs

def get_processing_time(ob_by_machine, machine_nb):
    pass

def is_free(tab, start, duration):
    pass

def find_first_available_place(start_ctr, duration, machine_jobs):
    pass

def decode(pb_instance, os, ms):
    pass

def translate_decoded_to_gantt(machine_operations):
    pass