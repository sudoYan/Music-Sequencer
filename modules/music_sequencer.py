from musicpy import *
from IPython.display import Audio, display, FileLink
import random
from time import sleep

def play_music(midi_file, settings, country = False):
    """Generates audio playback within output.
  
    Parameters
    ----------
    midi_file : musicpy.structures
      Musical structure to generate audio playback with
    settings : bool
      Whether settings are determined or not
    country : bool, default=False
      Whether music is country music
    """
    #Conditional to add settings and create midi file if settings are not determined
    if settings == False:
        if country == True:
          write(midi_file, bpm = 100, instrument = 25, name = 'output.mid')
        else:
          write(midi_file, bpm = 100, instrument = 1, name = 'output.mid')
    else:
        write(midi_file, name = 'output.mid')
  
    #Command to generate waveform audio file from midi file via Fluidsynth
    get_ipython().system('fluidsynth -F output.wav output.mid')
  
    #Play waveform audio file
    display(Audio('output.wav', autoplay=True))
    print('Loading')
    sleep(10)
    print('The file is now ready for download. Would you like to download it,' +
          ' or would you prefer to do so later?')
  
    #Conditional to allow download of files
    if take_user_input('Download now? [Y/N]: ', ['Y', 'N']) == 'Y':
        display(FileLink('output.wav'))
    else:
        print('Do remember: if you do not like the sequenced song,' +
              ' you can rerun sequencing through the Advanced Menu.')

class Genre():
    """Superclass to represent default musical instance.
  
    ...
  
    Attributes
    ----------
    name : str
      Name of the musical piece
    key_chord : str
      Note for key scale of piece
    add_to_chord : str
      Additional note regarding chord placement
    key_scale : musicpy.structures.scale
      Scale of the key chord arranged normally
    variation : int
      Number of variations and repetitions of progressions
    chord_tracks : list
      List of chord arpeggios arranged chronologically
    raw_chords : list
      List of chords unarpeggiated arranged chronologically
  
    Methods
    ----------
    generate_symph(inst_list_lead = range(1, 100), inst_list_rhyth, = range(1, 100).
    volumes = [80, 80, 70, 70, 70])
      Generates multi-instrumental playback.
    """
    def __init__(self, name, key_chord, add_to_chord, variation):
        self.name = name
        self.key_chord = key_chord
        self.add_to_chord = add_to_chord
        self.key_scale = scale(key_chord, add_to_chord)
        self.variation = variation
        self.chord_tracks = []
        self.raw_chords = []
  
    def generate_symph(self, inst_list_leads = random.sample(range(1, 70), 5),
                       inst_list_rhythm = random.sample(range(1, 70), 5),
                       volumes = [80, 80, 70, 70, 70]):
        """Generates multi-instrumental playback.
    
        Parameters
        ----------
        inst_list_leads, inst_list_rhythm : list, optional
          List of MIDI numbers of possible lead and rhythm instruments
        volumes : list, optional
          List of percentage values of instrument  volumes
    
        Returns
        ----------
        symph : musicpy.structures.piece
          Multi-instrumental MIDI piece
    
        Notes
        ----------
        Generates audio playback in output through play_music()
        """
        #Converts list of musicpy.structures.chord to construct tracklist
        chord_list = concat(self.chord_tracks)
        track_list = [chord_list, chord_list, chord_list, chord_list, chord_list]
    
        #Choose random acceptable instruments for playback and create list
        lead_inst = random.sample(inst_list_leads, 2)
        bg_inst = random.sample(inst_list_rhythm, 3)
        chosen_inst = [*lead_inst, *bg_inst]
    
        #Build pieces and add volume controls
        symph = piece(tracks = track_list, instruments = chosen_inst,
                      bpm = 120, start_times = [0, 0, 0, 0, 0])
    
        symph.add_volume(volumes[0], 0, mode = 'percentage', start_time = 0)
        symph.add_volume(volumes[1], 1, mode = 'percentage', start_time = 0)
        symph.add_volume(volumes[2], 2, mode = 'percentage', start_time = 0)
        symph.add_volume(volumes[3], 3, mode = 'percentage', start_time = 0)
        symph.add_volume(volumes[4], 4, mode = 'percentage', start_time = 0)
    
        #Plays music with pre-determined musical settings
        play_music(symph, True)
    
        return symph #musicpy.structures.piece returned
                       
class Jazz(Genre):
    """Subclass of Genre to represent all jazz instances.
  
    ...
  
    Attributes
    ----------
    name : str
      Name of the musical piece
    key_chord : str
      Note for key scale of piece
    add_to_chord : str
      Additional note regarding chord placement
    key_scale : musicpy.structures.scale
      Scale of the key chord arranged normally
    variation : int
      Number of variations and repetitions of progressions
    chord_tracks : list
      List of chord arpeggios arranged chronologically
    raw_chords : list
      List of chords unarpeggiated arranged chronologically
  
    Methods
    ----------
    sequence(rerun = False, change_key = False)
      Generates MIDI sequence of jazz
    generate_symph()
      Calls superclass generate_symph() method with instruments and volumes
    """
    def sequence(self, rerun = False, change_key = False):
        """Generates MIDI sequence of jazz
    
        Parameters
        ----------
        rerun : bool, default=False
          Whether to overwrite previous instance sequence
        change_key : bool, default=False
          Whether to change key scale within sequence
    
        Returns
        ----------
        self.chord_tracks : list
          List of musicpy.structures.chord arranged chronologically
    
        Notes
        ----------
        Generates audio playback in output through play_music()
        """
    
        progressions = [['5', '1'], ['2', '5'], ['2', '5', '1'],
         ['4', '5', '1'], ['1', '6', '2', '5']] #List of Jazz progressions
        count = 0 #initialise counter variable
    
        #Create local variables from instance attributes
        add_chord = self.add_to_chord
        key_scale = self.key_scale
    
        #Conditional to ensure callback on chord_tracks without overwriting original
        if self.chord_tracks == [] or rerun == True:
            #In case user wishes to overwrite musical piece
            self.chord_tracks = []
            self.raw_chords = []
      
          #Loop to add chord progressions in sets until count equals variation
            while count <= self.variation:
    
                #Divides acceptable progressions by 'minor' and 'major'
                if add_chord == 'minor':
                    prog = random.choice(progressions[0:3])
                else:
                    prog = random.choice(progressions)
      
                #Changes key of scale when 2 progressions are left
                if change_key == True and self.variation - count == 2:
                    key_scale = key_scale.down(2)
      
                #Loop to add chords from numbers listed in chord progressions
                for x in prog:
      
                    #Add characteristic unpredictability to jazz
                    if count%3 == 0:
                        add_chord_new = random.choice(['major', 'minor'])
        
                      #Sub-progression to transition to new chord type
                      if add_chord_new != add_chord:
                          x = '4'
                          self.raw_chords.append(get_chord(
                              key_scale.get_note_from_degree(int(x)), add_chord))
                          self.chord_tracks.append(arp(get_chord(
                              key_scale.get_note_from_degree(int(x)), add_chord),
                              random.randrange(2, 4), random.randrange(5, 7),
                              durations = 0.5, intervals = 0.0625, second_half = True))
                          add_chord = add_chord_new
        
                    #Conditional to add chords based on specified degree
                    if int(x) == 5:
                        chord_x = get_chord(key_scale.get_note_from_degree(int(x)), 'M7')
                        if add_chord == 'minor':
                          chord_x = chord_x('b9')
                    elif int(x) == 2:
                        chord_x = get_chord(key_scale.get_note_from_degree(int(x)), 'm7')
                        if add_chord == 'minor':
                          chord_x = chord_x('b5')
                    elif int(x) == 1 and add_chord == 'minor':
                        chord_x = get_chord(key_scale.get_note_from_degree(int(x)), 'm6')
                    else:
                        chord_x = get_chord(
                            key_scale.get_note_from_degree(int(x)), add_chord)
        
                    #Provide finger-based inversion to chords randomly
                    chord_x.inv(random.randrange(1, 3))
        
                    #Add chord to raw_chords and chord_tracks
                    self.raw_chords.append(chord_x)
                    self.chord_tracks.append(arp(chord_x,
                              random.randrange(2, 4), random.randrange(4, 7),
                              durations = 0.5, intervals = 0.0625, second_half = True))
      
                count += 1
    
        #Generate audio playback inside output without determined settings
        play_music(self.chord_tracks, False)
    
        return self.chord_tracks #return list of musicpy.structures.chord
  
def generate_symph(self):
    """Calls superclass generate_symph() method with instruments and volumes
    """
    super().generate_symph([1, 2, 3, 12, 26, 52],
         [27, 32, 40, 56, 57, 64, 65, 66], [85, 75, 70, 65, 55])
    
class Pop(Genre):
    """Subclass of Genre to represent all pop instances.
  
    ...
  
    Attributes
    ----------
    name : str
      Name of the musical piece
    key_chord : str
      Note for key scale of piece
    add_to_chord : str
      Additional note regarding chord placement
    key_scale : musicpy.structures.scale
      Scale of the key chord arranged normally
    variation : int
      Number of variations and repetitions of progressions
    chord_tracks : list
      List of chord arpeggios arranged chronologically
    raw_chords : list
      List of chords unarpeggiated arranged chronologically
  
    Methods
    ----------
    sequence(rerun = False)
      Generates MIDI sequence of jazz
    generate_symph()
      Calls superclass generate_symph() method with instruments and volumes
    """
  
    def sequence(self, rerun = False):
        """Generates MIDI sequence of pop.
    
        Parameters
        ----------
        rerun : bool, default=False
          Whether to overwrite previous instance sequence
    
        Returns
        ----------
        self.chord_tracks : list
          List of musicpy.structures.chord arranged chronologically
    
        Notes
        ----------
        Generates audio playback in output through play_music()
        """
        progressions = [['1', '5', '6', '4'], ['1', '6', '4', '5'],
        ['1', '4', '5'], ['1', '4', '6', '5'],
        ['6', '4', '1', '5'], ['1', '4', '1']] #List of pop progressions
    
        #Conditional to check whether to overwrite prior pop sequence
        if self.chord_tracks == [] or rerun == True:
            self.chord_tracks = []
            self.raw_chords = []
      
            #Choose a progression for the pop sequence
            prog = random.choice(progressions)
      
            #Loop to add chords based on degree in scale from progression
            for x in prog:
                add_chord = self.add_to_chord #reset local variable to instance value
        
                #Conditional to change add_chord based on degree from scale
                if int(x) == 6:
                    add_chord = 'minor'
        
                #Add chord to raw_chords and chord_tracks
                chord_x = get_chord(self.key_scale.get_note_from_degree(int(x)), add_chord)
                self.raw_chords.append(chord_x)
                self.chord_tracks.append(arp(chord_x,
                                random.randrange(2, 4), random.randrange(5, 7),
                                durations = 0.5, intervals = 0.125, second_half = False))
        
            #Repeat chord progression by variation
            self.chord_tracks = self.chord_tracks * self.variation
            self.raw_chords = self.raw_chords * self.variation
    
        #Generate audio playback in output without determined settings
        play_music(self.chord_tracks, False)
    
        return self.chord_tracks #Returns list of musicpy.structures.chord
    
    def generate_symph(self):
        """Calls superclass generate_symph() method with instruments and volumes.
        """
        super().generate_symph([1, 2, 3, 24, 25, 12, 26, 40, 54, 56, 57, 72, 73, 78, 80, 81, 85, 106, 107, 110],
         [5, 9, 27, 28, 32, 33, 34, 35, 41, 42, 52, 53, 64, 65, 66, 67, 91, 92, 95, 104], [90, 75, 65, 55, 55])

class Country(Genre):
    """Subclass of Genre to represent all country music instances.
  
    ...
  
    Attributes
    ----------
    name : str
      Name of the musical piece
    key_chord : str
      Note for key scale of piece
    add_to_chord : str
      Additional note regarding chord placement
    key_scale : musicpy.structures.scale
      Scale of the key chord arranged normally
    variation : int
      Number of variations and repetitions of progressions
    chord_tracks : list
      List of chord arpeggios arranged chronologically
    raw_chords : list
      List of chords unarpeggiated arranged chronologically
  
    Methods
    ----------
    sequence(rerun = False)
      Generates MIDI sequence of country music
    generate_symph()
      Calls superclass generate_symph() method with instruments and volumes
    """
  
    def sequence(self, rerun = False):
        """Generates MIDI sequence of country music.
    
        Parameters
        ----------
        rerun : bool, default=False
          Whether to overwrite previous instance sequence
    
        Returns
        ----------
        self.chord_tracks : list
          List of musicpy.structures.chord arranged chronologically
    
        Notes
        ----------
        Generates audio playback in output through play_music()
        """
        progressions = [['1', '4', '5'], ['1', '5', '4'], ['1', '5', '4', '6'],
         ['1', '4', '6', '5'], ['1', '2', '4']] #List of country music progressions
    
        count = 0 #Initialise counter variable
    
        #Conditional to check whether to overwrite country music sequence
        if self.chord_tracks == [] or rerun == True:
            self.chord_tracks = []
            self.raw_chords = []
      
            #Loop to add progressions to chord_tracks through random choice
            while count <= self.variation:
                prog = random.choice(progressions)
        
                #Loop to add chords based on degree of progression to scale
                for x in prog:
                    add_chord = self.add_to_chord
          
                    #Conditional to change chord types based on degree from scale
                    if x == '6':
                        add_chord = 'minor'
                    elif x == '2':
                        prior_chord = get_chord(
                            self.key_scale.get_note_from_degree(int(x)).down(), 'dim7')
                        self.raw_chords.append(prior_chord)
                        self.chord_tracks.append(arp(prior_chord,
                                  random.randrange(2, 4), random.randrange(4, 7),
                                  durations = 0.5, intervals = 0.125, second_half = False))
                        add_chord = 'minor'
          
                    chord_x = get_chord(self.key_scale.get_note_from_degree(int(x)),
                                        add_chord)
          
                    #Perform random finger-based chord inversions
                    chord_x.inv(random.randrange(1, 3))
          
                    #Add to raw_chords and chord_tracks
                    self.raw_chords.append(chord_x)
                    self.chord_tracks.append(arp(chord_x,
                                random.randrange(2, 4), random.randrange(4, 7),
                                durations = 0.5, intervals = 0.125, second_half = False))
          
                count += 1
    
        #Generate audio playback in output without settings for country music
        play_music(self.chord_tracks, False, True)
    
        return self.chord_tracks #Returns list of musicpy.structures.chord
    
    def generate_symph(self):
        """Calls superclass generate_symph() method with instruments and volumes.
        """
        super().generate_symph([1, 2, 21, 22, 24, 25, 72, 73, 78, 79, 105, 106, 107, 110],
         [9, 19, 27, 31, 32, 35, 36, 37, 64, 65, 66, 67], [90, 80, 65, 55, 55])

def mix_pieces(piece_1, piece_2, change_key = True):
    """Mixes two musical pieces together into one musical instance.
  
    Parameters
    ----------
    piece_1, piece_2 : Genre instance
      Musical instances to mix together
    change_key : bool, default=True
      Whether to change key chord or not
  
    Returns
    ----------
    out_instance : Genre instance
      Mixed musical instance of both pieces
  
    Notes
    ----------
    Generates audio playback in output through play_music()
    Creates default Genre class instance
    """
  
    #Set key to that of piece_1
    key_chord = piece_1.key_chord
  
    #Initialised transposed and mixed tracks
    trans_track = []
    mixed_track = []
  
    #Find amount of transposition between both musical instances
    transpose = N(key_chord).degree - N(piece_2.key_chord).degree
  
    #Conditional to tranpose based on bool change_key
    if change_key == True:
        #Transpose piece_2 upwards
        if transpose > 0:
            for c in piece_2.raw_chords:
                trans_track.append(c.up(transpose))
        #Transpose piece_2 downwards
        elif transpose < 0:
            for c in piece_2.raw_chords:
                transpose = transpose * -1
                trans_track.append(c.down(transpose))
    else:
        trans_track = piece_2.chord_tracks
  
    #Initialise boolean to switch main added progression
    switch_bool = True
  
    #Loop over chords of both instances to created mixed tracklist
    for c1, c2 in zip(piece_1.raw_chords, trans_track):
    
        #Conditional to choose which chord to add to mixed_track
        if switch_bool == True:
            mixed_track.append(arp(c1,
                            random.randrange(2, 4), random.randrange(5, 7),
                            durations = 0.5, intervals = 0.0625, second_half = True))
        else:
            mixed_track.append(arp(c2,
                            random.randrange(2, 4), random.randrange(5, 7),
                            durations = 0.5, intervals = 0.0625, second_half = True))
      
        #Conditional to switch progressions when both chords are essentially the same
        if c1.standardize().reset_octave(3) == c2.standardize().reset_octave(3):
            switch_bool = not switch_bool
    
    #Generate audio playback in output without determined settings
    play_music(mixed_track, False)
  
    #Create name for building Genre musical instance
    mixed_name = f"{piece_1.name} + {piece_2.name}"
    out_instance = Genre(mixed_name, key_chord, "major", piece_1.variation)
    out_instance.chord_tracks = mixed_track
    #Returns mixed musical Genre instance
    return out_instance
