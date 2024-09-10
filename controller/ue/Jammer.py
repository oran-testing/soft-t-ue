import yaml
import gnuradio
import statistics
import osmosdr
import sys
import numpy as np
import random
import time
import pathlib
import argparse

class Jammer:

    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            options = yaml.safe_load(file)

        # Assign values with defaults
        self.jammer = options.get("jammer", 1)  # Default: 1 (fixed jammer)
        self.method = options.get("jamming", "direct")  # direct | sensing
        self.waveform = options.get("waveform", "sin_c")  # sin_c | sin_f | gaussian
        self.power = options.get("power", 10)  # Default: 10 units of power (arbitrary)
        self.band = options.get("band", 1)  # Default: 1 (2.4 GHz)
        self.freq = options.get("freq", 2412e6)  # Default: 2412 MHz (2.4 GHz Wi-Fi)
        self.ch_dist = options.get("ch_dist", 20e6)  # Default: 20 MHz channel distance (Wi-Fi)
        self.allocation = options.get("allocation", 1)  # Default: 1 (first allocation)
        self.t_jamming = options.get("t_jamming", 5)  # Default: 5 seconds of jamming time
        self.t_sensing = options.get("t_jamming", 0.05)  # Default: 0.05 seconds of sensing time
        self.duration = options.get("duration", 60)  # Default: 60 seconds of operation
        self.samp_rate = options.get("samp_rate", 32e6)  # Default: 60 seconds of operation
        self.sdr_bandwidth = options.get("sdr_bandwidth", 10e7)  # Default: dafualt to Hackrf Bandwidth

        if self.t_jamming > self.duration:
            self.t_jamming = self.duration


        self.if_gain = 0
        self.rf_gain = 0

        self.set_gains()

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
        file_sink = gnuradio.blocks.file_sink(gr.sizeof_float * 1, 'output.bin', False)
        file_sink.set_unbuffered(True)

        tb.connect(osmosdr_source, low_pass_filter)
        tb.connect(low_pass_filter, complex_to_mag_squared)
        tb.connect(complex_to_mag_squared, file_sink)

        tb.start()
        time.sleep(self.duration)
        tb.stop()
        tb.wait()

        return 0.5 * statistics.mean(np.memmap("output.bin", mode="r", dtype=np.float32))


    def jam(self):

        self.samp_rate = 20e6  # Sample Rate
        self.sdr_bandwidth = 40e6  # Hackrf SDR Bandwidth
        set_gains()  # Hackrf SDR antenna gain

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
        if band == 1:
            self.ch_dist *= 10e5
        else:
            self.ch_dist = 20e6
        initial_freq, last_frequency = frequency_map[self.band - 1][self.allocation - 1]
        n_channels = (last_frequency - initial_freq) // self.ch_dist


        self.freq *= 10e5
        if self.method == "sensing" and sense(self.freq, self.t_sensing) < self.threshold:
            return 1

        jam(freq, waveform, power, t_jamming)

        return 0


    def jam_sequential(self):

        t_sensing = 0.05
        threshold = 0.0002

        channel = 1  # Initial Channel @ 2.412GHz
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.method == "sensing" and sense(self.freq, t_sensing) > threshold:
                continue
            set_frequency(channel, ch_dist)
            jam(self.freq, waveform, power, t_jamming)
            # Go to next channel
            channel = 1 if channel > n_channels else channel + 1

    def jam_random(self):

        start_time = time.time()
        while time.time() - start_time < duration:
            if self.method == "sensing" and sense(self.freq, t_sensing) > threshold:
                continue
            channel = random.randint(1, n_channels + 1)
            set_frequency(channel, ch_dist)
            jam(self.freq, waveform, power, t_jamming)


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

    return 0


if __name__ == "__main__":
   rc = main()
   sys.exit(rc)
