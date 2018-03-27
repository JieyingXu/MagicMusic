import mido
from mido import Message, MidiFile, MidiTrack

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=12, time=0))
track.append(Message('note_on', note=65, velocity=64, time=128))
# track.append(Message('note_off', note=65, velocity=127, time=256))

track.append(Message('note_on', note=64, velocity=64, time=128))
# track.append(Message('note_off', note=64, velocity=127, time=640))

mid.save('new_song.mid')
