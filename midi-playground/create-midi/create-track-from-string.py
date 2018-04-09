from mido import Message, MidiFile, MidiTrack, MetaMessage

mid = MidiFile()
track = MidiTrack()


# fname = "20th-century-fox.txt"
fname = "onlinesq-piano.txt"

with open(fname) as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        # print(line)

        if line.startswith("Track"):
            print(line)
            track = MidiTrack()
            mid.tracks.append(track)
        # elif line.startswith("program_change"):
        #     continue
        # elif line.startswith("control_change"):
        #     continue
        elif line.startswith("<meta"):
            continue
        else:
            print(line)
            msg = Message.from_str(line)
            track.append(msg)

mid.save("onlinesq-me.mid")