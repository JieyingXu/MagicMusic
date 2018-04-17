from mido import Message, MidiFile, MidiTrack, MetaMessage

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('instrument_name', name='102'))

fname = "glich.txt"
note_on_inputs = []

with open(fname) as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("note_on"):
            splits = line.split()
            channel = splits[1].split("=")[1]
            note = splits[2].split("=")[1]
            velocity = splits[3].split("=")[1]
            time = splits[4].split("=")[1]

            track.append(Message('note_on',
                                channel=int(channel),
                                note=int(note),
                                velocity=int(velocity),
                                time=int(time)))

        elif line.startswith("control_change"):
            splits = line.split()
            channel = splits[1].split("=")[1]
            control = splits[2].split("=")[1]
            value = splits[3].split("=")[1]
            time = splits[4].split("=")[1]

            track.append(Message('control_change',
                                 channel=int(channel),
                                 control=int(control),
                                 value=int(value),
                                 time=int(time)))

# for line in note_on_inputs:
#     splits = line.split()
#     channel = splits[1].split("=")[1]
#     note = splits[2].split("=")[1]
#     velocity = splits[3].split("=")[1]
#     time = splits[4].split("=")[1]
#
#     # print(line)
#     # print("channel:", channel, " note:", note, " velocity:", velocity, " time:", time)
#
#     track.append(Message('note_on', note=int(note), velocity=int(velocity), time=int(time)))

mid.save('glich.mid')