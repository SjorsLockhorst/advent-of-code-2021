from typing import Union, List, Dict
from dataclasses import dataclass


class InferenceException(Exception):
    pass


@dataclass
class Segment:
    encoded: str
    decoded: Union[str, None]


class Sequence:
    def __init__(self, segments: List[Segment], decoded: Union[int, None] = None):
        self.segments = segments
        self.decoded = decoded

    def __len__(self):
        return len(self.segments)


class DecodedSequence(Sequence):
    def __init__(self, sequences_str: List[str], decoder: Dict[str, Segment]):
        self.segments = [decoder[char] for char in sequences_str]
        self.decoded = self._decode()

    def _decoded_sequence(self):
        return set([segment.decoded for segment in self.segments if segment.decoded])

    def _decode(self) -> int:
        DECODED_MAPPINGS = [
            {"a", "b", "c", "e", "f", "g"},
            {"c", "f"},
            {"a", "c", "d", "e", "g"},
            {"a", "c", "d", "f", "g"},
            {"b", "c", "d", "f"},
            {"a", "b", "d", "f", "g"},
            {"a", "b", "d", "e", "f", "g"},
            {"a", "c", "f"},
            {"a", "b", "c", "d", "e", "f", "g"},
            {"a", "b", "c", "d", "f", "g"},
        ]
        decoded_sequence = self._decoded_sequence()
        for digit, dec_mapping in enumerate(DECODED_MAPPINGS):
            if dec_mapping == decoded_sequence:
                return digit
        raise Exception("No digit found")


def get_decoder(
    patterns: List[Sequence], segment_map: Dict[str, Segment]
) -> Dict[str, Segment]:

    sequence_map: Dict[int, Sequence] = {}

    # All sequences with a length of 5
    length_5 = [sequence for sequence in patterns if len(sequence) == 5]

    # All sequences with a length of 6
    length_6 = [sequence for sequence in patterns if len(sequence) == 6]

    # First inference:
    # Some digits that have unique amount of segments in sequence.
    for sequence in patterns:
        sequence_len = len(sequence)
        if sequence_len == 2:
            sequence.decoded = 1
            if 1 not in sequence_map:
                sequence_map[1] = sequence
            else:
                raise InferenceException(
                    f"Unexpectedly found multiple sequences with length {sequence_len}."
                )
        elif sequence_len == 3:
            sequence.decoded = 7
            if 7 not in sequence_map:
                sequence_map[7] = sequence
            else:
                raise InferenceException(
                    f"Unexpectedly found multiple sequences with length {sequence_len}."
                )
        elif sequence_len == 4:
            sequence.decoded = 4
            if 4 not in sequence_map:
                sequence_map[4] = sequence
            else:
                raise InferenceException(
                    f"Unexpectedly found multiple sequences with length {sequence_len}."
                )
        elif sequence_len == 7:
            sequence.decoded = 8
            if 8 not in sequence_map:
                sequence_map[8] = sequence
            else:
                raise InferenceException(
                    f"Unexpectedly found multiple sequences with length {sequence_len}."
                )

    # Second inference:
    # the segment in 7 not in 1 must be 'a'.
    found_2 = False
    for segment in sequence_map[7].segments:
        if segment not in sequence_map[1].segments:
            if found_2:
                raise InferenceException(
                    "Unexpectedly found 2 segments in 7 that are not in 1."
                )
            segment.decoded = "a"
            found_2 = True

    # Third inference:
    # Any sequence of length 6 that contains all segments of 4, must be 9.
    found_3 = False
    for sequence in length_6:
        has_all = True
        for segment in sequence_map[4].segments:
            if segment not in sequence.segments:
                has_all = False

        if has_all:
            if found_3:
                raise InferenceException(
                    "Unexpectedly found multiple sequences of length 6 that contain all segments of 4."
                )
            sequence.decoded = 9
            sequence_map[9] = sequence
            found_3 = True

    # Fourth inference:
    # The segment that is in 8 but not in 9 must be 'e'.
    found_4 = False
    for segment in sequence_map[8].segments:
        if segment not in sequence_map[9].segments:
            if found_4:
                raise InferenceException(
                    "Unexpectedly found two segments in 8 but not in 9."
                )
            segment.decoded = "e"
            found_4 = True

    # Fifth inference:
    # Any sequence of length 5 that contains 'e' must be 2.
    found_5 = False
    for sequence in length_5:
        for segment in sequence.segments:
            if segment.decoded == "e":
                if found_5:
                    raise InferenceException(
                        "Unexpectedly found multiple sequences of length 5 that contain 'e'."
                    )
                sequence.decoded = 2
                sequence_map[2] = sequence
                found_5 = True

    # Sixth inference:
    # The segment in 1 that is also in 2 must be 'c'.
    # The other segment in 1 must be 'f'.
    found_6 = False
    for segment in sequence_map[1].segments:
        if segment in sequence_map[2].segments:
            if found_6:
                raise InferenceException(
                    "Unexpectedly found multiple segments in 1 that are in two."
                )
            segment.decoded = "c"
        else:
            segment.decoded = "f"

    # Fetch only not yet decoded sequences.
    length_6 = [sequence for sequence in length_6 if not sequence.decoded]

    if not len(length_6) == 2:
        raise InferenceException(
            f"Unexpectedly found {len(length_6)} sequences with length 6, expected 2."
        )

    # Seventh inference:
    # Any unknown sequence of length 6 with 3 unknowns must be 6.
    # The only other unknown sequence left of length 6 must be 0.
    found_7 = False
    for sequence in length_6:
        total_unknown = len(sequence) - len(
            [segment for segment in sequence.segments if segment.decoded]
        )
        if total_unknown == 3:
            if found_7:
                raise InferenceException(
                    "Unexpectedly found 2 sequences of length 6 with 3 unknowns, expected only 1."
                )
            sequence.decoded = 6
            sequence_map[6] = sequence
            found_7 = True
        else:
            sequence.decoded = 0
            sequence_map[0] = sequence

    if not found_7:
        raise InferenceException(
            "Unexpectedly did not find any sequence of length 6 that had 3 unknown segments."
        )

    # Eigth inference:
    # The segment that is in 6 but not in 0 must be 'd'.
    found_8 = False
    for segment in sequence_map[6].segments:
        if segment not in sequence_map[0].segments:
            if found_8:
                raise InferenceException(
                    "Unexpectedly found multiple elements in in 6 but not in 0, expected 1."
                )
            segment.decoded = "d"
            found_8 = True

    if not found_8:
        raise InferenceException(
            "Unexpectedly did not find a segment in 6 that is not in 0. Expected 1."
        )

    # Tenth inference:
    # Last not yet decoded segment in 2 must be 'g'
    g_segment = [segment for segment in sequence_map[2].segments if not segment.decoded]
    if not len(g_segment) == 1:
        raise InferenceException(
            f"Unexpectedly found an incorrect number of un decoded segments in 2. Expected {1} found {len(g_segment)}"
        )
    g_segment[0].decoded = "g"

    # Last not yet decoded segment in 4 must be 'b'
    b_segment = [segment for segment in sequence_map[4].segments if not segment.decoded]
    if not len(b_segment) == 1:
        raise InferenceException(
            f"Unexpectedly found an incorrect number of un decoded segments in 4. Expected {1} found {len(b_segment)}"
        )
    b_segment[0].decoded = "b"

    return segment_map


# Get signal patterns
signal_patterns = []

# List of outputs that need to be decoded
outputs_to_decode = []

# List of dictionaries that maps each digit
segment_maps: List[Dict[str, Segment]] = []

f = open("input.txt")

# Read inputs
for line in f:
    segment_map: Dict[str, Segment] = {}

    values = line.strip().split("|")

    sequences = []

    for sequence_str in values[0].strip().split(" "):
        sequence = Sequence([])
        for segment_str in sequence_str:
            segment = None
            if segment_str not in segment_map:
                segment = Segment(segment_str, None)
                segment_map[segment_str] = segment
            else:
                segment = segment_map[segment_str]
            sequence.segments.append(segment)

        sequences.append(sequence)
    segment_maps.append(segment_map)
    signal_patterns.append(sequences)

    outputs_to_decode.append(values[1].strip().split(" "))


decoded_answers = []

for i in range(len(signal_patterns)):
    decoded_digits = []
    decoder = get_decoder(signal_patterns[i], segment_maps[i])
    output = outputs_to_decode[i]
    for sequence_str in output:
        decoded_sequence = DecodedSequence(sequence_str, decoder)
        decoded_digits.append(decoded_sequence.decoded)

    decoded_answer = int("".join([str(res) for res in decoded_digits]))
    decoded_answers.append(decoded_answer)

print(sum(decoded_answers))
