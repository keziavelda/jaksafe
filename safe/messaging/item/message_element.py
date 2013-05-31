"""
InaSAFE Disaster risk assessment tool developed by AusAid - **.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.
"""

__author__ = 'marco@opengis.ch'
__revision__ = '$Format:%H$'
__date__ = '27/05/2013'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')


class MessageElement():

    def __unicode__(self):
        return self.to_text()

    def __str__(self):
        return self.__unicode__()

    def _is_qstring(self, message):
        """Check if its a QString without adding any dep to PyQt4."""
        my_class = str(message.__class__)
        my_class_name = my_class.replace('<class \'', '').replace('\'>', '')
        if my_class_name == 'PyQt4.QtCore.QString':
            return True

        return False

    def to_html(self):
        """Render a MessageElement queue as html

        Args:
            None

        Returns:
            Str message the html representation of the message queue

        Raises:
            Errors are propagated
        """
        raise NotImplementedError('Please Implement this method')

    def to_text(self):
        """Render a MessageElement queue as text

        Args:
            None

        Returns:
            Str message the text representation of the message queue

        Raises:
            Errors are propagated
        """
        raise NotImplementedError('Please Implement this method')

    def to_markdown(self):
        """Render a MessageElement queue as markdown

        Args:
            None

        Returns:
            Str message the markdown representation of the message queue

        Raises:
            Errors are propagated
        """
        raise NotImplementedError('Please Implement this method')

    def to_json(self):
        """Render a MessageElement queue as JSON

        Args:
            None

        Returns:
            Str message the JSON representation of the message queue

        Raises:
            Errors are propagated
        """
        raise NotImplementedError('Please Implement this method')


class InvalidMessageItemError(Exception):
    """Custom exception for when the passed MessageElement is invalid."""
    pass