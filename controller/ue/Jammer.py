import sys
import time
import yaml
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import audio
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from statistics import mean
import osmosdr
import sys
import numpy as np
from random import randint
import time
import pathlib
import argparse

class Jammer:

    def __init__(self):
        self.IF_gain = 0
        self.RF_gain = 0
        self.freq = 0

    def sense(freq, duration):

        samp_rate = 32e6  # Delay before hopping to the next channel in sec
        sdr_bandwidth = 10e7  # Hackrf SDR Bandwidth

        tb = gr.top_block()

        osmosdr_source = osmosdr.source(args="numchan=1")

        osmosdr_source.set_time_unknown_pps(osmosdr.time_spec_t())
        osmosdr_source.set_sample_rate(samp_rate)
        osmosdr_source.set_center_freq(freq, 0)
        osmosdr_source.set_freq_corr(0, 0)
        osmosdr_source.set_gain(0, 0)
        osmosdr_source.set_if_gain(16, 0)
        osmosdr_source.set_bb_gain(16, 0)
        osmosdr_source.set_antenna('', 0)
        osmosdr_source.set_bandwidth(sdr_bandwidth, 0)

        # Inbetween blocks
        low_pass_filter = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                75e3,
                25e3,
                firdes.WIN_HAMMING,
                6.76))
        complex_to_mag_squared = blocks.complex_to_mag_squared(1)

        # Sink block
        file_sink = blocks.file_sink(gr.sizeof_float * 1, 'output.bin', False)
        file_sink.set_unbuffered(True)

        tb.connect(osmosdr_source, low_pass_filter)
        tb.connect(low_pass_filter, complex_to_mag_squared)
        tb.connect(complex_to_mag_squared, file_sink)

        tb.start()
        time.sleep(duration)
        tb.stop()
        tb.wait()


    def jam(self, freq, waveform, power, duration=1):

        print(f"\nThe frequency currently jammed is: {freq / (10e5)}MHz")
        samp_rate = 20e6  # Sample Rate
        sdr_bandwidth = 40e6  # Hackrf SDR Bandwidth
        RF_gain, IF_gain = set_gains(power)  # Hackrf SDR antenna gain

        tb = gr.top_block()

        if waveform == 1:
            source = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 1000, 1, 0, 0)
        elif waveform == 2:
            source = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 1000, 1, 0, 0)
        elif waveform == 3:
            source = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)
        else:
            print("invalid selection")

        freq_mod = analog.frequency_modulator_fc(1)
        osmosdr_sink = osmosdr.sink(args="numchan=1")
        osmosdr_sink.set_time_unknown_pps(osmosdr.time_spec_t())
        osmosdr_sink.set_sample_rate(samp_rate)
        osmosdr_sink.set_center_freq(freq, 0)
        osmosdr_sink.set_freq_corr(0, 0)
        osmosdr_sink.set_gain(RF_gain, 0)
        osmosdr_sink.set_if_gain(IF_gain, 0)
        osmosdr_sink.set_bb_gain(20, 0)
        osmosdr_sink.set_antenna('', 0)
        osmosdr_sink.set_bandwidth(sdr_bandwidth, 0)

        if waveform == 2:
            tb.connect(source, freq_mod, osmosdr_sink)
        else:
            tb.connect(source, osmosdr_sink)

        tb.start()
        time.sleep(duration)
        tb.stop()
        tb.wait()


    def set_frequency(self, channel, ch_dist):
        if channel == 1:
            self.freq = init_freq
        else:
            self.freq = init_freq + (channel - 1) * ch_dist



    def set_gains(self, power):
        if -40 <= power <= 5:
            self.RF_gain = 0
            if power < -5:
                self.IF_gain = power + 40
            elif -5 <= power <= 2:
                self.IF_gain = power + 41
            elif 2 < power <= 5:
                self.IF_gain = power + 42
        elif power > 5:
            self.RF_gain = 14
            self.IF_gain = power + 34
        else:
            raise ValueError("invalid Jammer Transmit power")



    def rx_from_mean(self):
        return 0.5 * mean(np.memmap("output.bin", mode="r", dtype=np.float32))


def parse():
    script_dir = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Run a Jammer or a channel Detector")
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=script_dir / "jammer.yaml",
        help="Config file path")
    return parser.parse_args()

def main():
    args = parse()

    with open(str(args.config), 'r') as file:
        options = yaml.safe_load(file)

    jammer = options.get("jammer")
    jamming = options.get("jamming")
    waveform = options.get("waveform")
    power = options.get("power")
    band = options.get("band")
    freq = options.get("freq")
    ch_dist = options.get("ch_dist")
    allocation = options.get("allocation")
    t_jamming = options.get("t_jamming")
    duration = options.get("duration")

    # Special options
    if jammer != 1:
        if band == 1:
            ch_dist = ch_dist * 10e5
            init_freq = 2412e6
            lst_freq = 2484e6
        elif band == 2:
            ch_dist = 20e6
            if allocation == 1:
                init_freq = 5180e6
                lst_freq = 5240e6
            elif allocation == 2:
                init_freq = 5260e6
                lst_freq = 5320e6
            elif allocation == 3:
                init_freq = 5500e6
                lst_freq = 5720e6
            elif allocation == 4:
                init_freq = 5745e6
                lst_freq = 5825e6
            else:
                print('Invalid selection')
                return 1
        else:
            print('Invalid selection')
            return 1
        n_channels = (lst_freq - init_freq) // ch_dist
        if t_jamming > duration:
            t_jamming = duration

    if jamming == 2:
        t_sensing = 0.05
        threshold = 0.0002

    # Starting RF Jamming
    if jammer == 1:
        freq = freq * 10e5
        if jamming == 1:
        	while (jamming):
        		time.sleep(2)
        		jam(freq, waveform, power, t_jamming)
        elif jamming == 2:
            # Sensing Channel
            sense(freq, t_sensing)
            rx_power = detect()
            print(rx_power)
            # If channel is active then jam it
            if rx_power > threshold:
                jam(freq, waveform, power, t_jamming)

        else:
            print("Invalid jamming option selection")
            return 1

    elif jammer == 2:
        channel = 1  # Initial Channel @ 2.412GHz
        start_time = time.time()
        while True:
            freq = set_frequency(channel, ch_dist)
            if jamming == 1:
                # Jam
                jam(freq, waveform, power, t_jamming)
            elif jamming == 2:
                # Sensing Channel
                sense(freq, t_sensing)
                rx_power = detect()
                # If channel is active then jam it
                if rx_power > threshold:
                    jam(freq, waveform, power, t_jamming)
            else:
                print("Invalid jamming option selection")
                return 1
            # Go to next channel
            channel = 1 if channel > n_channels else channel + 1
            # Checking elapsed time
            jamming_time_per_run = time.time() - start_time
            if jamming_time_per_run >= duration:
                break

    elif jammer == 3:
        start_time = time.time()
        while True:
            channel = randint(1, n_channels + 1)
            freq = set_frequency(channel, ch_dist)
            if jamming == 1:
                # Jam
                jam(freq, waveform, power, t_jamming)
            elif jamming == 2:
                # Sensing Channel
                sense(freq, t_sensing)
                rx_power = detect()
                # If channel is active then jam it
                if rx_power > threshold:
                    jam(freq, waveform, power, t_jamming)
            else:
                print("Invalid jamming option selection")
                return 1
                # Checking elapsed time
            jamming_time_per_run = time.time() - start_time
            if jamming_time_per_run >= duration:
                break

    else:
        print("invalid jammer selection")
        return 1
    return 0


if __name__ == "__main__":
   rc = main()
   sys.exit(rc)
