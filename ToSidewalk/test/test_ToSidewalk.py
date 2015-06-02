import unittest
import random
from ToSidewalk.ToSidewalk import *

class TestToSidewalkMethods(unittest.TestCase):
    def test_sort_nodes(self):
        """

        """
        center = "38.988152,-76.941595"
        center = map(float, center.split(","))
        center_node = Node('0', LatLng(center[0], center[1]))

        latlngs = """
38.988927,-76.940528
38.989269,-76.941408
38.988239,-76.942878
38.987172,-76.942540
38.987105,-76.941494
38.987906,-76.940222
        """

        latlngs = latlngs.strip().split('\n')
        latlngs = [map(float, latlng.split(',')) for latlng in latlngs]

        nodes1 = [Node(str(i), LatLng(latlng[0], latlng[1])) for i, latlng in enumerate(latlngs)]
        nodes2 = [Node(str(i), LatLng(latlng[0], latlng[1])) for i, latlng in enumerate(latlngs)]

        random.shuffle(nodes1)
        nodes1 = sort_nodes(center_node, nodes1)

        for node1, node2 in zip(nodes1, nodes2):
            self.assertTrue(node1.latlng == node2.latlng)

    def test_make_crosswalk_node(self):
        clat, clng = 0, 0
        lat1, lng1 = 0, 1
        lat2, lng2 = 1, 0
        cnode = Node('0', LatLng(clat, clng))
        node1 = Node('1', LatLng(lat1, lng1))
        node2 = Node('2', LatLng(lat2, lng2))

        const = 0.000001414
        rlat, rlng = const / math.sqrt(2), const / math.sqrt(2)
        node = make_crosswalk_node(cnode, node1, node2)
        self.assertEqual(rlat, node.latlng.lat)
        self.assertEqual(rlng, node.latlng.lng)

    def test_swap_nodes(self):
        pass

if __name__ == '__main__':
    unittest.main()
