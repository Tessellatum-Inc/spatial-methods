import math, unittest
from hmm_viterbi import viterbi_decode
class ViterbiTests(unittest.TestCase):
 def setUp(self):
  self.states=('Rainy','Sunny'); self.symbols=('walk','shop','clean')
  self.start=(0.6,0.4); self.trans=((0.7,0.3),(0.4,0.6)); self.emit=((0.1,0.4,0.5),(0.6,0.3,0.1))
 def test_classic_sequence(self):
  path,score=viterbi_decode(('walk','shop','clean'),self.states,self.symbols,self.start,self.trans,self.emit)
  self.assertEqual(path,['Sunny','Rainy','Rainy']); self.assertTrue(math.isfinite(score))
 def test_empty_sequence(self):
  self.assertEqual(viterbi_decode((),self.states,self.symbols,self.start,self.trans,self.emit),([],0.0))
 def test_zero_probability_sequence_rejected(self):
  with self.assertRaises(ValueError): viterbi_decode(('clean',),self.states,self.symbols,(1,0),self.trans,((1,0,0),(1,0,0)))
 def test_unknown_symbol(self):
  with self.assertRaises(ValueError): viterbi_decode(('unknown',),self.states,self.symbols,self.start,self.trans,self.emit)
 def test_bad_probability_sum(self):
  with self.assertRaises(ValueError): viterbi_decode(('walk',),self.states,self.symbols,(0.2,0.2),self.trans,self.emit)
 def test_dimension_mismatch(self):
  with self.assertRaises(ValueError): viterbi_decode(('walk',),self.states,self.symbols,self.start,((1,0),),self.emit)
 def test_tie_breaks_by_state_order(self):
  path,_=viterbi_decode(('x',),('first','second'),('x',),(0.5,0.5),((0.5,0.5),(0.5,0.5)),((1.0,),(1.0,)))
  self.assertEqual(path,['first'])
if __name__=='__main__':unittest.main()


class BaumWelchTests(unittest.TestCase):
 def setUp(self):
  self.states=('A','B'); self.symbols=('x','y')
  self.start=(0.6,0.4); self.trans=((0.8,0.2),(0.25,0.75)); self.emit=((0.9,0.1),(0.2,0.8))

 def test_forward_likelihood_matches_exhaustive_path_sum(self):
  from hmm_viterbi import forward_log_likelihood
  import itertools
  observations=('x','y','y'); total=0.0
  for path in itertools.product(range(2), repeat=len(observations)):
   probability=self.start[path[0]]*self.emit[path[0]][self.symbols.index(observations[0])]
   for t in range(1,len(path)):
    probability*=self.trans[path[t-1]][path[t]]*self.emit[path[t]][self.symbols.index(observations[t])]
   total+=probability
  self.assertAlmostEqual(forward_log_likelihood(observations,self.states,self.symbols,self.start,self.trans,self.emit),math.log(total),places=12)

 def test_baum_welch_increases_likelihood_and_normalises_parameters(self):
  from hmm_viterbi import baum_welch
  sequences=[('x','x','x','y','y','y')*4,('y','y','y','x','x','x')*3,('x','x','y','y')*4]
  start,trans,emit,history=baum_welch(sequences,self.states,self.symbols,(0.5,0.5),
    ((0.6,0.4),(0.4,0.6)),((0.6,0.4),(0.4,0.6)),max_iterations=80,tolerance=1e-9)
  self.assertGreater(history[-1],history[0])
  for row in (start,*trans,*emit): self.assertAlmostEqual(sum(row),1.0,places=10)
  self.assertTrue(all(math.isfinite(value) for value in history))

 def test_baum_welch_multiple_sequences_and_empty_sequences(self):
  from hmm_viterbi import baum_welch
  result=baum_welch([(),('x','y','x'),('y','y','x')],self.states,self.symbols,
    self.start,self.trans,self.emit,max_iterations=5)
  self.assertEqual(len(result[1]),2); self.assertEqual(len(result[2]),2)
  self.assertGreaterEqual(len(result[3]),2); self.assertLessEqual(len(result[3]),6)

 def test_baum_welch_rejects_invalid_inputs(self):
  from hmm_viterbi import baum_welch, forward_log_likelihood
  with self.assertRaises(ValueError): baum_welch([()],self.states,self.symbols,self.start,self.trans,self.emit)
  with self.assertRaises(ValueError): baum_welch([('z',)],self.states,self.symbols,self.start,self.trans,self.emit)
  with self.assertRaises(ValueError): baum_welch([('x',)],self.states,self.symbols,self.start,self.trans,self.emit,max_iterations=0)
  with self.assertRaises(ValueError): forward_log_likelihood(('x',),self.states,self.symbols,(1,0),self.trans,((0,1),(0,1)))
