from unittest import TestCase

from .tile_types import Connector, create_paired_connectors


class Test__Connectors(TestCase):
    
    def test__single_connector(self) -> None:
        """A standard single connector connects only to itself."""
        
        single = Connector('Single')
        self.assertEqual(single.connects_to, {single})
    
    
    def test__paired_connectors(self) -> None:
        """Paired connectors connect only to each other, not themselves."""
        
        positive, negative = create_paired_connectors('Paired')
        self.assertEqual(positive.connects_to, {negative})
        self.assertEqual(negative.connects_to, {positive})

