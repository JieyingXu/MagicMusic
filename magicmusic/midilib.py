from mido import *
from mido.messages import *
import mido
import os
import json
from django.conf import settings

soundfont_path = "media/audio/soundfonts/FluidR3_GM.sf2"

class MidiLib:

    # midi blob sample:
    #
    # c3,2.3,5.1
    # c4,4.0,7.0
    # <key startposition duration>
    # return a list of tuples
    # <"on/off", notekey, offset>
    @staticmethod
    def parse_midi_offset_from_blob(midi_blob):
        strip =  midi_blob.strip()
        lines = strip.split("\n")

        # will sort everything
        note_messages = []

        for line in lines:
            splits = line.strip().split(',')
            note_key = splits[0]
            start = float(splits[1])    # absolute time
            duration = float(splits[2])
            end = start + duration  # absolute time

            note_messages.append(("on", note_key, start))
            note_messages.append(("off", note_key, end))

        # additional note off at the end
        # note_messages.append(("off", note_key, 0.1))

        sorted_note_messages = sorted(note_messages, key=lambda tuple: tuple[2])


        offset_note_messages = []
        # print sorted message in an offset manner
        for i, message in enumerate(sorted_note_messages):
            if i == 0:
                offset_note_messages.append(message)
            else:
                offset = message[2] - sorted_note_messages[i-1][2]
                offset_note_messages.append((message[0], message[1], offset))

        return offset_note_messages

    # multipler will be used to magnify the time offset, e.g. 96
    @staticmethod
    def format_mido_onoffs_default_velocity(offset_note_messages, channel, multiplier):
        onoffs = ""
        for message in offset_note_messages:
            type = "note_" + message[0]
            note_key = message[1]
            offset = message[2]
            time = int(multiplier*offset)   # time must be int


            message = Message(type, channel=channel, time=time,
                              note=MidiLib.convert_note_key_to_num(note_key),
                              velocity=127)

            line = str(message) + "\n"
            onoffs += line

        lastnote="note_off channel=" + str(channel) + " note=56 velocity=127 time=180\n"
        onoffs += lastnote

        return onoffs

    @staticmethod
    def save_one_track_to_wav(filename ,global_metadata, track_metadata, formatted_onoffs):
        midFile = mido.MidiFile()
        track = mido.MidiTrack()
        midFile.tracks.append(track)

        instrument_number = MidiLib.get_instrument_number(track_metadata)

        # change instrument
        track.append(mido.Message(type='program_change', channel=0, program=instrument_number, time=0))
        for line in formatted_onoffs.strip().split("\n"):
            msg = mido.Message.from_str(line)
            print(line)
            track.append(msg)

        # save to midi file
        midFilePath = 'media/audio/runtime-wavs/'+filename+'.mid'
        midFile.save(midFilePath)

        # save to wav file
        # fluid_synth = midi2audio.FluidSynth(soundfont_path)
        wavFilePath = 'media/audio/runtime-wavs/'+filename+'.wav'
        os.system('fluidsynth -g 2.5 -ni ' + soundfont_path + ' '
        + midFilePath + ' -F ' + wavFilePath + ' -r 44100 > /dev/null')
        # fluid_synth.midi_to_audio(midFilePath, wavFilePath)



        return wavFilePath

    @staticmethod
    def save_all_track_to_wav(filename, global_metadata, track_info_list):
        midFile = mido.MidiFile()
        for info in track_info_list:
            channel = int(info['channel'])
            instrument = str(info['instrument']).lower()
            print("got instrument:", instrument)
            instrument_number = MidiLib.translate_instrument_number(instrument)
            print("instrument number:", instrument_number)
            blob = info['blob']

            # add to track
            track = mido.MidiTrack()
            midFile.tracks.append(track)

            # change instrument
            track.append(mido.Message(type='program_change', channel=channel,
                                      program=instrument_number, time=0))
            if blob != None:
                parsed_onoffs = MidiLib.parse_midi_offset_from_blob(str(json.loads(blob)['blob']))
                formatted_onoffs = MidiLib.format_mido_onoffs_default_velocity(parsed_onoffs, channel, 96).strip()
                for line in formatted_onoffs.split("\n"):
                    msg = mido.Message.from_str(line)
                    track.append(msg)

        # save to midi file
        midFilePath = 'media/audio/runtime-wavs/' + filename + '.mid'
        midFile.save(midFilePath)

        # generate wav
        wavFilePath = 'media/audio/runtime-wavs/' + filename + '.wav'
        os.system('fluidsynth -g 2.5 -ni ' + soundfont_path + ' '
                  + midFilePath + ' -F ' + wavFilePath + ' -r 44100 > /dev/null')

        return wavFilePath


    @staticmethod
    def generate_unit_notes_if_not_exists(instrument_name):
        instrument_number = MidiLib.translate_instrument_number(instrument_name)
        file_prefix = "ins_" + str(instrument_number) + "_nt_"

        unit_urls = []
        for i in range(0, 128):
            filename = file_prefix + str(i)
            midFilePath = 'media/audio/runtime-wavs/' + filename + '.mid'
            wavFilePath = 'media/audio/runtime-wavs/' + filename + '.wav'

            # check exists
            checkpath = settings.MEDIA_ROOT + '/audio/runtime-wavs/' + filename + '.wav'
            if os.path.exists(checkpath):
                unit_urls.append(wavFilePath)
                continue

            # save to midi file
            midFile = mido.MidiFile()
            track = mido.MidiTrack()
            midFile.tracks.append(track)
            track.append(mido.Message(type='program_change', channel=0,
                                      program=instrument_number, time=0))
            track.append(mido.Message(type='note_on', channel=0,
                                      note=i, time=0))
            track.append(mido.Message(type='note_off', channel=0,
                                      note=i, time=96))
            track.append(mido.Message(type='note_off', channel=0,
                                      note=i, time=180))

            # save to midi file
            midFile.save(midFilePath)
            # generate wav
            os.system('fluidsynth -g 2.5 -ni ' + soundfont_path + ' '
                      + midFilePath + ' -F ' + wavFilePath + ' -r 44100 > /dev/null')

            unit_urls.append(wavFilePath)

        return unit_urls


    # https://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python
    # Input is string in the form C#-4, Db-4, or F-3. If your implementation doesn't use the hyphen,
    # just replace the line :
    #    letter = midstr.split('-')[0].upper()
    # with:
    #    letter = midstr[:-1]
    @staticmethod
    def convert_note_key_to_num(midstr):
        Notes = [["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"], ["F"],
                 ["F#", "Gb"], ["G"], ["G#", "Ab"], ["A"], ["A#", "Bb"], ["B"]]
        answer = 0
        i = 0
        # Note
        letter = midstr[:-1]
        for note in Notes:
            for form in note:
                if letter.upper() == form:
                    answer = i
                    break;
            i += 1
        # Octave
        answer += (int(midstr[-1])) * 12
        return answer

    @staticmethod
    def get_instrument_number(track_metadata):
        if 'instrument' not in track_metadata:
            return 0
        instrument_name = str(track_metadata['instrument']).lower()
        return MidiLib.translate_instrument_number(instrument_name)

    @staticmethod
    def translate_instrument_number(instrument_name):
        if instrument_name == 'guitar':
            return 24
        elif instrument_name == "drum":
            return 118
        else:
            return 0
