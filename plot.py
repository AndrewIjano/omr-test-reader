'''
    Plots graphs from the experiment
'''

import json
import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import statistics

plt.rcParams.update({'font.size': 12, 'figure.figsize': (10, 10)})


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the experiments")
    return parser.parse_args()


def get_processed_data(file):
    data = json.loads(file.read())

    successes = [int(i['success']) for i in data]
    times = [i['time'] for i in data]
    times_pixels = [i['time'] / i['pixels'] for i in data]

    return {
        'len': len(data),
        'success_count': 100*sum(successes) / len(successes),
        'time_mean': statistics.mean(times),
        'time_stdev': statistics.stdev(times),
        'time_pixels_mean': statistics.mean(times_pixels),
        'time_pixels_stdev': statistics.stdev(times_pixels)
    }


args = get_args()
path = args.path

with (
    open(f'{path}/scans-simple.json') as simple_1_f,
    open(f'{path}/scans2-simple.json') as simple_2_f,
    open(f'{path}/scans-doh.json') as doh_1_f,
    open(f'{path}/scans2-doh.json') as doh_2_f
):
    x_pos = [1, 2]

    simple_1_data = get_processed_data(simple_1_f)
    simple_2_data = get_processed_data(simple_2_f)
    doh_1_data = get_processed_data(doh_1_f)
    doh_2_data = get_processed_data(doh_2_f)

    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
    ax1 = fig.add_subplot(spec[0, 0])
    ax2 = fig.add_subplot(spec[0, 1])
    ax3 = fig.add_subplot(spec[1, 0])

    simple_success_counts = [
        simple_1_data['success_count'], simple_2_data['success_count']]
    doh_success_counts = [doh_1_data['success_count'],
                          doh_2_data['success_count']]
    labels = ['scans', 'scans2']

    x = np.arange(len(labels))
    width = 0.35

    rects1 = ax1.bar(x - width/2, simple_success_counts,
                     width, alpha=0.5, label='Simple')
    rects2 = ax1.bar(x + width/2, doh_success_counts,
                     width, alpha=0.5, label='DoH')

    ax1.set_ylabel('Códigos lidos com sucesso (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.yaxis.grid(True)

    ax1.legend()

    plt.tight_layout()

    simple_times = [simple_1_data['time_mean'], simple_2_data['time_mean']]
    simple_times_stdev = [simple_1_data['time_stdev'],
                          simple_2_data['time_stdev']]
    doh_times = [doh_1_data['time_mean'], doh_2_data['time_mean']]
    doh_times_stdev = [doh_1_data['time_stdev'], doh_2_data['time_stdev']]

    labels = ['scans', 'scans2']

    x = np.arange(len(labels))
    width = 0.35

    time_means_simple = ax2.bar(x - width/2, simple_times, width, yerr=simple_times_stdev,
                                align='center', alpha=0.5, ecolor='black', capsize=10, label='Simple')
    time_means_doh = ax2.bar(x + width/2, doh_times, width, yerr=doh_times_stdev,
                             align='center', alpha=0.5, ecolor='black', capsize=10, label='DoH')

    ax2.set_ylabel('Tempo médio de execução (s)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.yaxis.grid(True)

    ax2.legend()

    simple_time_pixels = [simple_1_data['time_pixels_mean'],
                          simple_2_data['time_pixels_mean']]
    simple_time_pixels_stdev = [
        simple_1_data['time_pixels_stdev'], simple_2_data['time_pixels_stdev']]
    doh_time_pixels = [doh_1_data['time_pixels_mean'],
                       doh_2_data['time_pixels_mean']]
    doh_time_pixels_stdev = [
        doh_1_data['time_pixels_stdev'], doh_2_data['time_pixels_stdev']]

    labels = ['scans', 'scans2']

    x = np.arange(len(labels))
    width = 0.35

    time_pixel_means_simple = ax3.bar(x - width/2, simple_time_pixels, width, yerr=simple_time_pixels_stdev,
                                      align='center', alpha=0.5, ecolor='black', capsize=10, label='Simple')
    time_pixel_means_doh = ax3.bar(x + width/2, doh_time_pixels, width, yerr=doh_time_pixels_stdev,
                                   align='center', alpha=0.5, ecolor='black', capsize=10, label='DoH')

    ax3.set_ylabel('Tempo médio de execução por pixel da imagem (s)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels)
    ax3.yaxis.grid(True)

    ax3.legend()

    plt.tight_layout()

    plt.savefig('plot.png')
    plt.show()
