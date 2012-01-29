import polyomino as mino
import unittest
import cProfile

class TestPolyomino(unittest.TestCase):
    def setUp(self):
        # Test is this guy:
        # [][][]
        # []
        self.test_mino = mino.Polyomino([(0,0), (0,1), (0,2), (1,0)])
        
    def test_rotations_reflections(self):
        # Check rotations
        rot_left = mino.Polyomino([(0,0),(1,0),(2,0),(2,1)])
        rot_half = mino.Polyomino([(0,2),(1,0),(1,1),(1,2)])
        rot_right = mino.Polyomino([(0,0),(0,1),(1,1),(2,1)])

        self.assertEqual(rot_left, self.test_mino.rotate_left())
        self.assertEqual(rot_half, self.test_mino.rotate_half())
        self.assertEqual(rot_right, self.test_mino.rotate_right())

        # Test rotations()
        self.assertEqual({self.test_mino, rot_left, rot_half, rot_right},
                         set(self.test_mino.rotations()),
                         msg="The rotations() function doesn't work.")

        # Check reflections
        ref_horiz = mino.Polyomino([(0,0),(0,1),(0,2),(1,2)])
        ref_vert = mino.Polyomino([(0,0),(1,0),(1,1),(1,2)])
        ref_diag = mino.Polyomino([(0,0),(0,1),(1,0),(2,0)])
        ref_skew = mino.Polyomino([(0,1),(1,1),(2,0),(2,1)])

        self.assertEqual(ref_vert, self.test_mino.reflect_vert())
        self.assertEqual(ref_horiz, self.test_mino.reflect_horiz())
        self.assertEqual(ref_diag, self.test_mino.reflect_diag())
        self.assertEqual(ref_skew, self.test_mino.reflect_skew())

        # Test transforms()
        self.assertEqual({self.test_mino, rot_left, rot_half, rot_right,
                          ref_horiz, ref_vert, ref_diag, ref_skew},
                         set(self.test_mino.transforms()),
                         msg="transforms() doesn't work.")

    def test_shape(self):
        h_exp, w_exp = expected = (2, 3)
        self.assertEqual(expected, self.test_mino.shape,
                         msg="Wrong shape")
        self.assertEqual(h_exp, self.test_mino.height,
                         msg="Wrong height")
        self.assertEqual(w_exp, self.test_mino.width,
                         msg="Wrong width")

    def test_grid(self):
        expected = [[True, True, True],[True, False, False]]
        self.assertEqual(expected, self.test_mino.grid(),
                         msg="Wrong grid representation")

    def test_str(self):
        pstr = str(self.test_mino)
        expected = "[][][]\n[]    "
        self.assertEqual(expected, pstr,
                         msg="Wrong repr: {0}".format(pstr))

    def test_generate(self):
        # Check sizes of the generation
        sizes_fixed = [0, 1, 2, 6, 19, 63, 216, 760, 2725, 9910]
        sizes_onesided = [0, 1, 1, 2, 7, 18, 60, 196, 704, 2500]
        sizes_free = [0, 1, 1, 2, 5, 12, 35, 108, 369, 1285]
        for i in range(10):
            minos = mino.generate(i)
            minos_onesided = mino.one_sided(minos)
            minos_free = mino.free(minos)
            self.assertEqual(sizes_fixed[i], len(minos),
                             msg="Wrong fixed size for n={0}".format(i))
            self.assertEqual(sizes_onesided[i], len(minos_onesided),
                             msg="Wrong onesided size for n={0}".format(i))
            self.assertEqual(sizes_free[i], len(minos_free),
                             msg="Wrong free size for n={0}".format(i))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPolyomino)
    unittest.TextTestRunner(verbosity=2).run(suite)
