import json
import csv
import os


def parse_pulse_periods(file_path, chanel:int):
    pulse_periods = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for i in range(5):
            next(reader)  # Skip header row if there is one

        previous_timestamp = None
        for row in reader:
            timestamp, *signals = row
            signal = signals[chanel]
            timestamp = float(timestamp)
            signal = int(signal)

            if signal == 1:
                if previous_timestamp is not None:
                    pulse_period = timestamp - previous_timestamp
                    pulse_periods.append(pulse_period)
                previous_timestamp = timestamp

    return pulse_periods


def get_params_from_name(name: str) -> float:
    return float('.'.join(name.split('_mm_')[0].split('_')))


if __name__ == '__main__':
    dir_path = './valid-data'
    data = {}
    for filename in os.listdir(dir_path):

        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            distance = get_params_from_name(file_path.lstrip(dir_path + '\\'))
            pulse_periods = parse_pulse_periods(file_path, 2)
            data[distance] = pulse_periods.copy()

    with open(f'pulses_data.json', 'w') as file:
        json.dump(data, file, indent=4)

