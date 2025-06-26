import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from murdf.urdf import (
    Umass, Uinertia, Uinertial,
    Ugeometry, Ucollision,
    Ulink, Urdf
)

def test_add_link_inertial_and_collision():
    mass = Umass(1.0)
    inertia = Uinertia([1,2,3,4,5,6])
    inertial = Uinertial(mass, inertia)
    geometry = Ugeometry('box', [1,1,1])
    collision = Ucollision(geometry)
    link = Ulink('test', None, inertial, collision)
    root = ET.Element('robot')
    Urdf.add_link(root, link)
    link_elem = root.find('link')
    assert link_elem is not None
    inertial_elem = link_elem.find('inertial')
    collision_elem = link_elem.find('collision')
    # inertial info should be under <inertial> tag
    assert inertial_elem is not None
    assert inertial_elem.find('mass') is not None
    # collision geometry should be under <collision> tag
    assert collision_elem is not None
    assert collision_elem.find('box') is not None
