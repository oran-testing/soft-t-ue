import yaml
import threading
import gnuradio
import statistics
import osmosdr
import sys
import numpy as np
import random
import time
import pathlib
import argparse
import threading
from gnuradio import analog


class Channel:

    def __init__(self, config_file="",
                 jam_type="fixed",
                 method="direct",
                 waveform="sin_c",
                 power=10,
                 band=1,
                 freq=2412e6,
                 ch_dist=20e6,
                 allocation=1,
                 t_jamming=5,
                 t_sensing=0.05,
                 duration=60,
                 samp_rate=32e6,
                 sdr_bandwidth=10e7,
                 output_path="output.bin"):

        self.jam_type = jam_type
        self.method =  method
        self.waveform =  waveform
        self.power =  power
        self.band =  band
        self.freq =  freq
        self.ch_dist =  ch_dist
        self.allocation =  allocation
        self.t_jamming =  t_jamming
        self.t_sensing =  t_sensing
        self.duration =  duration
        self.samp_rate =  samp_rate
        self.sdr_bandwidth =  sdr_bandwidth
        self.output_path = output_path

        if config_file:
            with open(config_file, 'r') as file:
                options = yaml.safe_load(file)

            # Assign values with defaults
            self.jam_type = options.get("jam_type", self.jam_type)  # Default: fixed | sequential | random
            self.method = options.get("jamming", self.method)  # direct | sensing
            self.waveform = options.get("waveform", self.waveform)  # sin_c | sin_f | gaussian
            self.power = options.get("power", self.power)  # Default: 10 units of power (arbitrary)
            self.band = options.get("band", self.band)  # Default: 1 (2.4 GHz)
            self.freq = options.get("freq", self.freq)  # Default: 2412 MHz (2.4 GHz Wi-Fi)
            self.ch_dist = options.get("ch_dist", self.ch_dist)  # Default: 20 MHz channel distance (Wi-Fi)
            self.allocation = options.get("allocation", self.allocation)  # Default: 1 (first allocation)
            self.t_jamming = options.get("t_jamming", self.t_jamming)  # Default: 5 seconds of jamming time
            self.t_sensing = options.get("t_sensing", self.t_sensing)  # Default: 0.05 seconds of sensing time
            self.duration = options.get("duration", self.duration)  # Default: 60 seconds of operation
            self.samp_rate = options.get("samp_rate", self.samp_rate)  # Default: 60 seconds of operation
            self.sdr_bandwidth = options.get("sdr_bandwidth", self.sdr_bandwidth)  # Default: dafualt to Hackrf Bandwidth
            self.output_path = options.get("output_path", self.output_path)  # Default: dafualt to Hackrf Bandwidth


        if self.t_jamming > self.duration:
            self.t_jamming = self.duration
        self.if_gain = 0
        self.rf_gain = 0
        self.set_gains()
        self.threads = []

    def sense(self):

        tb = gr.top_block()

        osmosdr_source = osmosdr.source(args="numchan=1")

        osmosdr_source.set_time_unknown_pps(osmosdr.time_spec_t())
        osmosdr_source.set_sample_rate(self.samp_rate)
        osmosdr_source.set_center_freq(self.freq, 0)
        osmosdr_source.set_freq_corr(0, 0)
        osmosdr_source.set_gain(0, 0)
        osmosdr_source.set_if_gain(16, 0)
        osmosdr_source.set_bb_gain(16, 0)
        osmosdr_source.set_antenna('', 0)
        osmosdr_source.set_bandwidth(self.sdr_bandwidth, 0)

        # Inbetween blocks
        low_pass_filter = gnuradio.filter.fir_filter_ccf(
            1,
            gnuradio.firdes.low_pass(
                1,
                self.samp_rate,
                75e3,
                25e3,
                gnuradio.firdes.WIN_HAMMING,
                6.76))
        complex_to_mag_squared = gnuradio.blocks.complex_to_mag_squared(1)

        # Sink block
        # NOTE: vector_sink may be more efficient
        # vector_sink = gnuradio.blocks.vector_sink_f()
        file_sink = gnuradio.blocks.file_sink(gr.sizeof_float * 1, self.output_path, False)
        file_sink.set_unbuffered(True)

        tb.connect(osmosdr_source, low_pass_filter)
        tb.connect(low_pass_filter, complex_to_mag_squared)
        tb.connect(complex_to_mag_squared, file_sink)

        tb.start()
        time.sleep(self.duration)
        tb.stop()
        tb.wait()

        return 0.5 * statistics.mean(np.memmap(self.output_path, mode="r", dtype=np.float32))


    def jam(self):

        self.samp_rate = 20e6  # Sample Rate
        self.sdr_bandwidth = 40e6  # Hackrf SDR Bandwidth

        tb = gnuradio.gr.top_block()

        if self.waveform == "sin_c":
            source = gnuradio.analog.sig_source_c(self.samp_rate, gnuradio.analog.GR_SIN_WAVE, 1000, 1, 0, 0)
        elif self.waveform == "sin_f":
            source = gnuradio.analog.sig_source_f(self.samp_rate, gnuradio.analog.GR_SIN_WAVE, 1000, 1, 0, 0)
        elif self.waveform == "gaussian":
            source = gnuradio.analog.noise_source_c(gnuradio.analog.GR_GAUSSIAN, 1, 0)
        else:
            raise ValueError("invalid waveform")

        freq_mod = analog.frequency_modulator_fc(1)
        osmosdr_sink = osmosdr.sink(args="numchan=1")
        osmosdr_sink.set_time_unknown_pps(osmosdr.time_spec_t())
        osmosdr_sink.set_sample_rate(self.samp_rate)
        osmosdr_sink.set_center_freq(self.freq, 0)
        osmosdr_sink.set_freq_corr(0, 0)
        osmosdr_sink.set_gain(self.rf_gain, 0)
        osmosdr_sink.set_if_gain(self.if_gain, 0)
        osmosdr_sink.set_bb_gain(20, 0)
        osmosdr_sink.set_antenna('', 0)
        osmosdr_sink.set_bandwidth(self.sdr_bandwidth, 0)

        if waveform == "sin_f":
            tb.connect(source, freq_mod, osmosdr_sink)
        else:
            tb.connect(source, osmosdr_sink)

        tb.start()
        time.sleep(self.duration)
        tb.stop()
        tb.wait()


    def set_frequency(self, channel, ch_dist):
        if channel == 1:
            self.freq = init_freq
        else:
            self.freq = init_freq + (channel - 1) * ch_dist



    def set_gains(self):
        if -40 <= self.power <= 5:
            self.rf_gain = 0
            if self.power < -5:
                self.if_gain = self.power + 40
            elif -5 <= self.power <= 2:
                self.if_gain = self.power + 41
            elif 2 < self.power <= 5:
                self.if_gain = self.power + 42
        elif self.power > 5:
            self.rf_gain = 14
            self.rf_gain = self.power + 34
        else:
            raise ValueError("invalid Jammer Transmit power")


    def jam_fixed(self):

        frequency_map = [
            [(2412e6, 2484e6)], # Band 1 2.4 GHz
            [(5180e6, 5240e6),(5260e6,5320e6),(5500e6,5720e6),(5745e6, 5825e6)] # Band 2 5 GHz
        ]
        if self.band == 1:
            self.ch_dist *= 10e5
        else:
            self.ch_dist = 20e6
        initial_freq, last_frequency = frequency_map[self.band - 1][self.allocation - 1]
        n_channels = (last_frequency - initial_freq) // self.ch_dist


        self.freq *= 10e5
        if self.method == "sensing" and self.sense(self.freq, self.t_sensing) < self.threshold:
            return 1

        self.jam()

        return 0


    def jam_sequential(self):

        t_sensing = 0.05
        threshold = 0.0002

        channel = 1  # Initial Channel @ 2.412GHz
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.method == "sensing" and self.sense(self.freq, t_sensing) > threshold:
                continue
            set_frequency(channel, ch_dist)
            self.jam()
            # Go to next channel
            channel = 1 if channel > n_channels else channel + 1

    def jam_random(self):

        start_time = time.time()
        while time.time() - start_time < duration:
            if self.method == "sensing" and self.sense(self.freq, t_sensing) > threshold:
                continue
            channel = random.randint(1, n_channels + 1)
            set_frequency(channel, ch_dist)
            self.jam()

    def run_threaded(self, func, *args, **kwargs):
        #thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        #thread.start()
        #self.threads.append(thread)
        func()


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
    jammer_t = Channel()
    jammer_t.run_threaded(getattr(jammer_t, "jam_" + jammer_t.jam_type))

    return 0


if __name__ == "__main__":
   rc = main()
   sys.exit(rc)
