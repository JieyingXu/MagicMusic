from mido import Message, MidiFile, MidiTrack, MetaMessage

mid = MidiFile()
track = MidiTrack()


fname = "20th-century-fox.txt"

with open(fname) as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        print(line)

        if line.startswith("Track"):
            track = MidiTrack()
            mid.tracks.append(track)
        elif line.startswith("<meta"):
            continue
        else:
            msg = Message.from_str(line)
            track.append(msg)

mid.save("test.mid")