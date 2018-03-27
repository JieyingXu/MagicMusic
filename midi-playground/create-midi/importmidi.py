from mido import MidiFile

# mid = MidiFile('the-pink-panther-original.mid')
mid = MidiFile('20th-century-fox.mid')
# mid = MidiFile('track7.mid')
mid = MidiFile('test.mid')

f = open("test.txt", "w")

for i, track in enumerate(mid.tracks):
    # if i == 7:
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         print(msg)

    print('Track {}: {}'.format(i, track.name))
    f.write('Track {}: {}'.format(i, track.name) + '\n')
    for msg in track:
        print(msg)
        f.write(str(msg)+"\n")

f.close()