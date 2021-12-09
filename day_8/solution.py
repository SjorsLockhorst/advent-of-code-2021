from pprint import pprint
from typing import Union, Dict
from dataclasses import dataclass

f = open("test.txt")
# f = open("input.txt")


def part_1():
    signal_patterns = []
    outputs = []

    for line in f:
        values = line.strip().split("|")

        signal_patterns.append([num for num in values[0].split(" ") if num])

        outputs.append([num for num in values[1].split(" ") if num])

    unique_amounts = [2, 4, 3, 7]

    total = 0

    for vals in outputs:
        for val in vals:
            if len(val) in unique_amounts:
                total += 1

    print(total)


@dataclass
class Segment:

    encoded: str
    decoded: Union[str, None]


@dataclass
class Sequence:

    segment_map: Dict[str, Segment]
    decoded: Union[int, None]

    def get_encoded_sequence(self):
        return "".join([seg_str for seg_str in self.segment_map.keys()])

    def get_decoded_sequence(self):
        return "".join(
            [
                segment.decoded
                for segment in self.segment_map.values()
                if segment.decoded
            ]
        )

    def __len__(self):
        return len(self.segment_map)


signal_patterns = []

outputs = []

for line in f:
    values = line.strip().split("|")

    sequences = []

    for sequence_str in values[0].strip().split(" "):
        sequence = Sequence({}, None)
        for segment_str in sequence_str:
            segment = None
            if segment_str not in sequence.segment_map:
                segment = Segment(segment_str, None)
                sequence.segment_map[segment_str] = segment
            else:
                segment = sequence.segment_map[segment_str]

        sequences.append(sequence)
    signal_patterns.append(sequences)


test_patterns = signal_patterns[0]

sequence_map = {}
for sequence in test_patterns:
    sequence_len = len(sequence)
    if sequence_len == 2:
        sequence.decoded = 1
        sequence_map[1] = sequence
    elif sequence_len == 3:
        sequence.decoded = 7
        sequence_map[7] = sequence
    elif sequence_len == 4:
        sequence.decoded = 4
        sequence_map[4] = sequence
    elif sequence_len == 7:
        sequence.decoded = 8
        sequence_map[8] = sequence

for segment in sequence_map[7].segment_map.values():
    if segment not in sequence_map[1].segment_map.values():
        segment.decoded = "a"

length_6 = [sequence for sequence in test_patterns if len(sequence) == 6]

for sequence in length_6:
    has_all = True
    for segment in sequence_map[4].segment_map.values():
        if segment not in sequence.segment_map.values():
            has_all = False

    if has_all:
        sequence.decoded = 9
        sequence_map[9] = sequence
        break

for segment in sequence_map[8].segment_map.values():
    if segment not in sequence_map[9].segment_map.values():
        segment.decoded = "e"

# TODO: continue with next line
pprint(sequence_map)
