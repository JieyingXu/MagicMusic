from mido import MidiFile

# mid = MidiFile('the-pink-panther-original.mid')
mid = MidiFile('20th-century-fox.mid')
# mid = MidiFile('track7.mid')

f = open("20th-century-fox.txt", "w")

for i, track in enumerate(mid.tracks):
    # if i == 7:
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         print(msg)

    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)
        f.write(str(msg)+"\n")

f.close()