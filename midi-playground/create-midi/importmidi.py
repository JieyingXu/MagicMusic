from mido import MidiFile

# mid = MidiFile('the-pink-panther-original.mid')
mid = MidiFile('track7.mid')

for i, track in enumerate(mid.tracks):
    # if i == 7:
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         print(msg)

    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)