class MidiLib:

    # midi blob sample:
    #
    # c3 2.3 5.1
    # c4 4.0 7.0
    # <key startposition duration>
    @staticmethod
    def parse_midi_json(midi_blob):
        lines = midi_blob.strip().split("\n")

        # will sort everything
        note_messages = []

        for line in lines:
            splits = line.strip().split()
            note_key = splits[0]
            start = float(splits[1])    # absolute time
            duration = float(splits[2])
            end = start + duration  # absolute time

            note_messages.append(("on", note_key, start))
            note_messages.append(("off", note_key, end))

        sorted_note_messages = sorted(note_messages, key=lambda tuple: tuple[2])

        print(sorted_note_messages)

        offset_note_messages = []
        # print sorted message in an offset manner
        for i, message in enumerate(sorted_note_messages):
            if i == 0:
                offset_note_messages.append(message)
            else:
                offset = message[2] - sorted_note_messages[i-1][2]
                offset_note_messages.append((message[0], message[1], offset))

        print(offset_note_messages)


