import music_sequencer as ms
class TestJazzSequence():
  """Test sequence() method of Jazz Class"""

  #Test instances
  jazz_one = ms.Jazz('Lovers Blues', 'Db', 'minor', 6)
  jazz_two = ms.Jazz('World of Wonder', 'F#', 'major', 4)
  output_one = jazz_one.sequence()
  output_two = jazz_two.sequence()

  def test_one(self):
    """Test type of output of sequence()"""
    assert type(self.output_one) == list
    assert type(self.output_two) == list
    assert self.output_one, self.output_two != []
    
  def test_two(self):
    """Test type of list elements of sequence()"""
    for item in self.output_one:
      assert type(item) == musicpy.structures.chord
    for item in self.output_two:
      assert type(item) == musicpy.structures.chord
      
  def test_three(self):
    """Test overwrite capabilities of sequence()"""
    new_output = self.jazz_one.sequence()
    for item1, item2 in zip(new_output, self.output_one):
      assert item1 == item2
    new_output = self.jazz_two.sequence(rerun = True)
    assert new_output != self.output_two
    
class TestGenerateSymph():
  """Test generate_symph() method of Genre superclass"""

  #Test instances
  music = ms.Genre('Music', 'C#', 'major', 4)
  music.chord_tracks = ms.Pop('Pop', 'C#', 'major', 4).sequence()
  
  def test_one(self):
    """Test type of output of generate_symph()"""
    assert type(self.music.generate_symph()) == musicpy.structures.piece
      
class TestMixPieces():
  """Test mix_pieces() function"""

  #Test instances
  piece_1 = ms.Jazz('Lacrimost', 'G', 'major', 6)
  piece_2 = ms.Pop('Iraet', 'F', 'major', 5)
  piece_1.sequence()
  piece_2.sequence()
  
  def test_one(self):
    """Test type of output of mix_pieces()"""
    assert type(ms.mix_pieces(self.piece_1, self.piece_2)) == Genre
    
  def test_two(self):
    """Test whether chord tracks is filled by mix_pieces()"""
    output = ms.mix_pieces(self.piece_1, self.piece_2)
    assert type(output.chord_tracks) == list
    assert output.chord_tracks != [] 
    for item in output.chord_tracks:
      assert type(item) == musicpy.structures.chord
      
  def test_three(self):
    output = ms.mix_pieces(self.piece_1, self.piece_2)
    assert type(output.name) == str
    assert output.name == self.piece_1.name + ' + ' + self.piece_2.name
