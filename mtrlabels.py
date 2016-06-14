#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
import simplestyle

class MTRLabels(inkex.Effect):
    """
    Example Inkscape effect extension.
    Creates a new layer with a "Hello World!" text centered in the middle of the document.
    """
    def __init__(self):
        """
        Constructor.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)

    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method.
        """

        for id,node in self.selected.iteritems():
            self.setStyle(node)

    def setStyle(self, node):
        style = simplestyle.parseStyle(node.get('style'))

        style['text-align'] = 'center'
        style['text-anchor'] = 'middle'
        style['font-family'] = '\'Myriad Pro\''
        style['font-size'] = '6.25px'

        # Unset styles on original
        style.pop('fill', None)
        style.pop('stroke', None)

        node.set('style', simplestyle.formatStyle(style))

        id = node.get('id')
        parent = node.getparent()

        parent.remove(node)

        group = inkex.etree.SubElement(parent, 'g')

        group.append(node)

        outline = inkex.etree.SubElement(group, 'use')
        outline.set(inkex.addNS('href', 'xlink'), '#%s' % id)
        outline.set('style', simplestyle.formatStyle({'stroke': '#ffffff'}))

        text = inkex.etree.SubElement(group, 'use')
        text.set(inkex.addNS('href', 'xlink'), '#%s' % id)
        text.set('style', simplestyle.formatStyle({'fill': '#00234f'}))

# Create effect instance and apply it.
effect = MTRLabels()
effect.affect()