import unittest
from src.fpvf_soul_shell_legacy import FPVFSystem

class LegacyFPVFTests(unittest.TestCase):
    def test_phi_normalization_is_bounded(self):
        s=FPVFSystem(condensation=3)
        for n in range(12):
            self.assertGreater(s.phi(n),-1.0);self.assertLess(s.phi(n),1.0)

    def test_equal_legacy_scores_have_equilibrium_one(self):
        self.assertAlmostEqual(FPVFSystem().equilibrium(1.0,1.0),1.0)

    def test_memory_accumulates_in_process(self):
        s=FPVFSystem()
        self.assertEqual(s.update_memory(2,0.5),1.0)
        self.assertEqual(len(s.state["memory"]),1)

    def test_void_gate_threshold_matches_source_heuristic(self):
        s=FPVFSystem()
        self.assertFalse(s.void_gate(0.5,0)[1]);self.assertTrue(s.void_gate(1.1,0)[1])

    def test_step_advances_counter(self):
        s=FPVFSystem();s.step(1,0)
        self.assertEqual(s.state["n"],1)
        self.assertIn("C",s.state["last"])

if __name__=="__main__":unittest.main()
