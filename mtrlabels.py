#!/usr/bin/env python

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
        textcontent = inkex.etree.tostring(node, method="text", encoding="UTF-8").strip().decode("utf-8")

        style = simplestyle.parseStyle(node.get('style'))

        is_chinese = ord(textcontent[0]) > 256

        style['text-align'] = 'center'
        style['text-anchor'] = 'middle'
        style['font-family'] = '\'MTR Sung\'' if is_chinese else '\'Myriad Pro\''
        style['font-size'] = '7.5px' if is_chinese else '6.25px'
        style['font-weight'] = 'normal' if is_chinese else '600'

        # Unset styles on original
        style.pop('fill', None)
        style.pop('stroke', None)

        node.set('style', simplestyle.formatStyle(style))

        id = node.get('id')
        parent = node.getparent()
        index = parent.index(node)

        parent.remove(node)

        group = inkex.etree.Element('g')

        parent.insert(index, group)

        text = inkex.etree.SubElement(group, 'text')
        text.set('id', id)
        text.set('style', simplestyle.formatStyle(style))
        (x, y) = self.getXY(node)
        text.set('x', str(x))
        text.set('y', str(y))
        text.text = textcontent

        outline = inkex.etree.SubElement(group, 'use')
        outline.set(inkex.addNS('href', 'xlink'), '#%s' % id)
        outline.set('style', simplestyle.formatStyle({'stroke': '#ffffff'}))

        fill = inkex.etree.SubElement(group, 'use')
        fill.set(inkex.addNS('href', 'xlink'), '#%s' % id)
        fill.set('style', simplestyle.formatStyle({'fill': '#00234f'}))

    def getXY(self, node):
        x = node.get('x')
        y = node.get('y')

        if(x is None or x is 0):
            for child in node:
                (x, y) = self.getXY(child)
                if(x is not None and x is not 0):
                    break

        return (x, y)

# Create effect instance and apply it.
effect = MTRLabels()
effect.affect()