#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
# 2024.08.31 Created by T.Ishigaki

"""Utilities for composing URDF elements and writing XML trees."""

import xml.etree.ElementTree as ET
import warnings


class Ugeometry:
    """Geometry primitive such as box, cylinder, or sphere."""

    type: str
    values: list

    def __init__(self, type_, values_):
        self.type = type_
        self.values = values_

    @staticmethod
    def add_param(parent, g):
        geometry = ET.SubElement(parent, g.type)
        if g.type == "box":
            if len(g.values) == 3:
                geometry.set("size", ", ".join(map(str, g.values)))
            else:
                warnings.warn(
                    "missing values' list length should be 3 but " + str(len(g.values))
                )
        elif g.type == "cylinder":
            if len(g.values) == 2:
                geometry.set("radius", str(g.values[0]))
                geometry.set("length", str(g.values[1]))
            else:
                warnings.warn(
                    "missing values' list length should be 2 but " + str(len(g.values))
                )
        elif g.type == "sphere":
            if len(g.values) == 1:
                geometry.set("radius", str(g.values[0]))
            else:
                warnings.warn(
                    "missing values' list length should be 1 but " + str(len(g.values))
                )
        else:
            warnings.warn("missing geometry type : " + g.type)


class Ucolor:
    """Color definition used by a material."""

    type: str
    values: list

    def __init__(self, type_, values_):
        self.type = type_
        self.values = values_

    @staticmethod
    def add_param(parent, c):
        color = ET.SubElement(parent, "color")
        color.set(c.type, ", ".join(map(str, c.values)))


class Umaterial:
    """Material definition combining a name and color."""

    name: str
    color: Ucolor

    def __init__(self, name_, color_):
        self.name = name_
        self.color = color_

    @staticmethod
    def add_param(parent, m):
        material = ET.SubElement(parent, "material")
        material.set("name", str(m.name))
        Ucolor.add_param(material, m.color)


class Uorigin:
    """Pose information with position and orientation."""

    xyz: list
    rpy: list

    def __init__(self, xyz_, rpy_):
        self.xyz = xyz_
        self.rpy = rpy_

    @staticmethod
    def add_param(parent, o):
        origin = ET.SubElement(parent, "origin")
        origin.set("xyz", ", ".join(map(str, o.xyz)))
        origin.set("rpy", ", ".join(map(str, o.rpy)))


class Umass:
    """Mass value in kilograms."""

    value: float

    def __init__(self, value_):
        self.value = value_

    @staticmethod
    def add_param(parent, m):
        mass = ET.SubElement(parent, "mass")
        mass.set("value", str(m.value))


class Uinertia:
    """Inertia matrix values."""

    values: float

    def __init__(self, values_):
        self.values = values_

    @staticmethod
    def add_param(parent, m):
        inertia = ET.SubElement(parent, "inertia")
        if len(m.values) == 6:
            inertia.set("ixx", str(m.values[0]))
            inertia.set("ixy", str(m.values[1]))
            inertia.set("ixz", str(m.values[2]))
            inertia.set("iyy", str(m.values[3]))
            inertia.set("iyz", str(m.values[4]))
            inertia.set("izz", str(m.values[5]))
        else:
            warnings.warn(
                "missing values' list length should be 6 but " + str(len(m.values))
            )


class Uaxis:
    """Axis definition used by joints."""

    type: str
    values: list

    def __init__(self, type_, values_):
        self.type = type_
        self.values = values_

    @staticmethod
    def add_param(parent, a):
        origin = ET.SubElement(parent, "origin")
        origin.set(a.type, ", ".join(map(str, a.values)))


class Ulimit:
    """Joint limits for motion and effort."""

    lower: float
    upper: float
    effort: float
    velocity: float

    def __init__(self, lower_, upper_, effort_, velocity_):
        self.lower = lower_
        self.upper = upper_
        self.effort = effort_
        self.velocity = velocity_

    @staticmethod
    def add_param(parent, l):
        limit = ET.SubElement(parent, "limit")
        limit.set("lower", str(l.lower))
        limit.set("upper", str(l.upper))
        limit.set("effort", str(l.effort))
        limit.set("velocity", str(l.velocity))


class Uvisual:
    """Visual element describing geometry and appearance."""

    geometry: Ugeometry
    material: Umaterial
    origin: Uorigin

    def __init__(self, geometry_, material_, origin_=None):
        if origin_ is None:
            origin_ = []
        self.geometry = geometry_
        self.material = material_
        self.origin = origin_

    @staticmethod
    def add_param(parent, visual):
        v = ET.SubElement(parent, "visual")
        if visual.geometry:
            Ugeometry.add_param(v, visual.geometry)
        if visual.material:
            Umaterial.add_param(v, visual.material)
        if visual.origin:
            Uorigin.add_param(v, visual.origin)


class Ucollision:

    """Collision element used for contact calculations."""

    geometry: Ugeometry
    origin: Uorigin

    def __init__(self, geometry_, origin_=None):
        if origin_ is None:
            origin_ = []
        self.geometry = geometry_
        self.origin = origin_

    @staticmethod
    def add_param(parent, collision):
        c = ET.SubElement(parent, "collision")
        if collision.geometry:
            Ugeometry.add_param(c, collision.geometry)
        if collision.origin:
            Uorigin.add_param(c, collision.origin)


class Uinertial:
    """Inertial properties of a link."""

    mass: Umass
    inertia: Uinertia
    origin: Uorigin

    def __init__(self, mass_, inertia_, origin_=None):
        if origin_ is None:
            origin_ = []
        self.mass = mass_
        self.inertia = inertia_
        self.origin = origin_

    @staticmethod
    def add_param(parent, inertial):
        i = ET.SubElement(parent, "inertial")
        if inertial.mass:
            Umass.add_param(i, inertial.mass)
        if inertial.inertia:
            Uinertia.add_param(i, inertial.inertia)
        if inertial.origin:
            Uorigin.add_param(i, inertial.origin)


class Ulink:
    """URDF link combining visual, collision, and inertial data."""


    name: str
    visual: Uvisual
    collision: Ucollision
    inertial: Uinertial

    def __init__(
        self,
        name_,
        visual_,
        inertial_=None,
        collision_=None,
    ):
        if inertial_ is None:
            inertial_ = []
        if collision_ is None:
            collision_ = []
        self.name = name_
        self.visual = visual_
        self.inertial = inertial_
        self.collision = collision_


class Ujoint:
    """URDF joint connecting two links."""

    name: str
    type: str
    axis: Uaxis
    p_link_name: str
    c_link_name: str
    limit: Ulimit
    origin: Uorigin


    def __init__(self, name_, type_, axis_, p_name_, limit_=None, c_name_=None, origin_=None):
        if limit_ is None:
            limit_ = []
        if c_name_ is None:
            c_name_ = []
        if origin_ is None:
            origin_ = []
        self.name = name_
        self.type = type_
        self.axis = axis_
        self.p_link_name = p_name_
        self.c_link_name = c_name_
        self.limit = limit_
        self.origin = origin_


class Urdf:
    """Helpers to append link and joint elements to an XML tree."""


    @staticmethod
    def add_link(parent, link):
        child = ET.SubElement(parent, "link")
        child.set("name", link.name)
        if link.visual:
            Uvisual.add_param(child, link.visual)
        if link.inertial:
            Uinertial.add_param(child, link.inertial)
        if link.collision:
            Ucollision.add_param(child, link.collision)

        return child

    @staticmethod
    def add_joint(parent, joint):
        j = ET.SubElement(parent, "joint")
        j.set("name", joint.name)
        j.set("type", joint.type)
        if joint.axis:
            Uaxis.add_param(j, joint.axis)
        if joint.limit:
            Ulimit.add_param(j, joint.limit)
        if joint.origin:
            Uorigin.add_param(j, joint.origin)
        if joint.p_link_name:
            p_name = ET.SubElement(j, "parent")
            p_name.set("link", joint.p_link_name)
        if joint.c_link_name:
            c_name = ET.SubElement(j, "child")
            c_name.set("link", joint.c_link_name)
        return j
