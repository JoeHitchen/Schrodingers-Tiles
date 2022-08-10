from unittest import TestCase

from .tile_types import Connector, create_paired_connectors, create_stub_connector


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
    
    
    def test__stub_connector(self) -> None:
        """Stub connectors connect to the main connector, but not to themselves."""
        
        main = Connector('Main')
        stub = create_stub_connector(main)
        self.assertEqual(main.connects_to, {main, stub})
        self.assertEqual(stub.connects_to, {main})

