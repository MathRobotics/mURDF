import unittest
import xml.etree.ElementTree as ET

from murdf import (
    Ugeometry,
    Ucolor,
    Umaterial,
    Uorigin,
    Umass,
    Uinertia,
    Uaxis,
    Ulimit,
    Uvisual,
    Ucollision,
    Uinertial,
    Ulink,
    Ujoint,
    Urdf,
)


class TestUrdfHelpers(unittest.TestCase):
    def test_ugeometry_box(self):
        root = ET.Element("root")
        Ugeometry.add_param(root, Ugeometry("box", [1, 2, 3]))
        elem = root.find("box")
        self.assertIsNotNone(elem)
        self.assertEqual(elem.get("size"), "1, 2, 3")

    def test_visual_and_material(self):
        root = ET.Element("root")
        visual = Uvisual(
            Ugeometry("box", [1, 1, 1]),
            Umaterial("steel", Ucolor("rgba", [1, 0, 0, 1])),
            Uorigin([0, 0, 0], [0, 0, 0]),
        )
        Uvisual.add_param(root, visual)
        v = root.find("visual")
        self.assertIsNotNone(v)
        self.assertIsNotNone(v.find("box"))
        material = v.find("material")
        self.assertIsNotNone(material)
        self.assertEqual(material.get("name"), "steel")
        color = material.find("color")
        self.assertIsNotNone(color)
        self.assertEqual(color.get("rgba"), "1, 0, 0, 1")
        self.assertIsNotNone(v.find("origin"))

    def test_add_link_and_joint(self):
        root = ET.Element("robot")
        visual = Uvisual(Ugeometry("box", [1, 1, 1]), None)
        link = Ulink("base", visual)
        link_elem = Urdf.add_link(root, link)
        self.assertEqual(link_elem.tag, "link")
        self.assertEqual(link_elem.get("name"), "base")
        self.assertIsNotNone(link_elem.find("visual"))

        joint = Ujoint(
            "joint1",
            "revolute",
            Uaxis("xyz", [0, 0, 1]),
            "base",
            Ulimit(-1, 1, 10, 2),
            "child",
            Uorigin([0, 0, 0], [0, 0, 0]),
        )
        joint_elem = Urdf.add_joint(root, joint)
        self.assertEqual(joint_elem.tag, "joint")
        self.assertEqual(joint_elem.get("type"), "revolute")
        self.assertIsNotNone(joint_elem.find("origin"))
        self.assertEqual(joint_elem.find("parent").get("link"), "base")
        self.assertEqual(joint_elem.find("child").get("link"), "child")
        self.assertIsNotNone(joint_elem.find("limit"))

    def test_inertia_param(self):
        root = ET.Element("root")
        Uinertia.add_param(root, Uinertia([1, 2, 3, 4, 5, 6]))
        elem = root.find("inertia")
        self.assertIsNotNone(elem)
        self.assertEqual(elem.get("ixx"), "1")
        self.assertEqual(elem.get("izz"), "6")


if __name__ == "__main__":
    unittest.main()
