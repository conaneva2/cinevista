"""Host-only tests. Passing these never certifies a Sony camera feature."""
import math
import random
import unittest
from geometry_reference import fit_display, plan_frame


class GeometryTests(unittest.TestCase):
    def test_xpan_crop(self):
        p = plan_frame(7952, 5304, target_aspect=65/24)
        self.assertEqual((p.output_width, p.output_height), (7952, 2936))
        self.assertAlmostEqual(p.source_crop.height, 7952 * 24 / 65)

    def test_natural_18(self):
        p = plan_frame(6000, 4000, 1.8)
        self.assertAlmostEqual(p.target_aspect, 2.7)
        self.assertAlmostEqual(p.retained_area_fraction, 1)
        self.assertEqual((p.output_width, p.output_height), (6000, 2222))

    def test_expand_is_interpolation(self):
        p = plan_frame(6000, 4000, 1.8, output_policy="expanded")
        self.assertEqual((p.output_width, p.output_height), (10800, 4000))
        self.assertEqual(p.source_crop.width, 6000)

    def test_xpan_is_not_270(self):
        p = plan_frame(6000, 4000, 1.8, 65/24)
        self.assertLess(p.source_crop.height, 4000)
        self.assertNotEqual(p.target_aspect, 2.7)

    def test_crop_sides(self):
        p = plan_frame(6000, 4000, 2.0, 2.39)
        self.assertAlmostEqual(p.source_crop.width, 4780)
        self.assertAlmostEqual(p.source_crop.height, 4000)

    def test_crop_vertical_offsets(self):
        a = plan_frame(6000, 4000, 1, 2.39, offset_y=-1)
        b = plan_frame(6000, 4000, 1, 2.39, offset_y=1)
        self.assertAlmostEqual(a.source_crop.top, 0)
        self.assertAlmostEqual(b.source_crop.bottom, 4000)

    def test_crop_horizontal_offsets(self):
        a = plan_frame(6000, 4000, 2, 2.39, offset_x=-1)
        b = plan_frame(6000, 4000, 2, 2.39, offset_x=1)
        self.assertAlmostEqual(a.source_crop.left, 0)
        self.assertAlmostEqual(b.source_crop.right, 6000)

    def test_output_cap(self):
        p = plan_frame(7952, 5304, 1, 65/24, output_width=6000)
        self.assertEqual(p.output_width, 6000)
        self.assertEqual(p.output_height, 2215)

    def test_no_automatic_upscale(self):
        p = plan_frame(6000, 4000, 1, 2.39, output_width=9000)
        self.assertEqual(p.output_width, 6000)

    def test_invalid_values(self):
        cases = [dict(width=0), dict(width=6000.1), dict(height=True),
                 dict(squeeze=float("nan")), dict(squeeze=0.9),
                 dict(target_aspect=float("inf")), dict(offset_x=2),
                 dict(offset_y=float("nan")), dict(output_policy="magic"),
                 dict(output_width=0), dict(offset_x=None), dict(squeeze=True)]
        for kw in cases:
            args = dict(width=6000, height=4000)
            args.update(kw)
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                plan_frame(**args)

    def test_orientation_is_not_faked(self):
        for orientation in range(2, 9):
            with self.subTest(orientation=orientation), self.assertRaises(ValueError):
                plan_frame(6000, 4000, orientation=orientation)

    def test_display_fit_square_pixels(self):
        r = fit_display(2.39, 640, 480)
        self.assertAlmostEqual(r.width, 640)
        self.assertAlmostEqual(r.width/r.height, 2.39)

    def test_display_fit_non_square_pixels(self):
        # Hypothetical test canvas, NOT an A7R II measured specification.
        pixel_aspect = 1.5 / (640/480)
        r = fit_display(65/24, 640, 480, pixel_aspect)
        self.assertAlmostEqual(r.width/r.height * pixel_aspect, 65/24)

    def test_randomized_geometry_10000(self):
        rng = random.Random(20260918)
        for i in range(10000):
            w, h = rng.randint(100, 12000), rng.randint(100, 12000)
            s, r = rng.uniform(1, 2.5), rng.uniform(1.5, 3.6)
            p = plan_frame(w, h, s, r, rng.uniform(-1, 1), rng.uniform(-1, 1))
            c = p.source_crop
            self.assertGreaterEqual(c.left, -1e-7)
            self.assertGreaterEqual(c.top, -1e-7)
            self.assertLessEqual(c.right, w+1e-7)
            self.assertLessEqual(c.bottom, h+1e-7)
            self.assertAlmostEqual(c.width*s/c.height, r, places=9)
            self.assertTrue(math.isclose(c.width, w) or math.isclose(c.height, h))
            self.assertGreater(p.retained_area_fraction, 0)
            self.assertLessEqual(p.retained_area_fraction, 1+1e-10)
            self.assertGreaterEqual(p.output_width, 2)
            self.assertGreaterEqual(p.output_height, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
