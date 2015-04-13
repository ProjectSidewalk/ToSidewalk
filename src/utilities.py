from imposm.parser import OSMParser
import pprint

try:
    from xml.etree import cElementTree as ET
except ImportError, e:
    from xml.etree import ElementTree as ET

pp = pprint.PrettyPrinter(indent=2)


class WaySearcher(object):
    def __init__(self, filename):
        self.filename = filename
        self.ways_found = []
        self.way_nodes = []
        self.key_values = []

    def find_ways(self, key_values):
        self.key_values = key_values
        p = OSMParser(concurrency=4, ways_callback=self.way_callback)
        p.parse(self.filename)

        self.ways_found = list(set(self.ways_found)) # delete duplicates.
        self.way_nodes = list(set(self.way_nodes))

        return self

    def key_values_exist(self, tags):
        """
        This method
        """
        for key, value in self.key_values:
            if key in tags:
                if value and value != tags[key]:
                    # If value is not None and it does not agree with tags[key],
                    return False
            else:
                return False
        return True

    def get_osm(self):
        ret = "<osm>\n"
        with open(self.filename, "rb") as osm:
            # Find element
            # http://stackoverflow.com/questions/222375/elementtree-xpath-select-element-based-on-attribute
            tree = ET.parse(osm)
            # print tree.find(".//way[@id='%d']" % self.ways_found[0])
            ret += ET.tostring(tree.find(".//bounds"))
            for node_id in self.way_nodes:
                ret += ET.tostring(tree.find(".//node[@id='%d']" % node_id))
            for way_id in self.ways_found:
                ret += ET.tostring(tree.find(".//way[@id='%d']" % way_id))
        ret += "</osm>"
        return ret

    def get_ways(self):
        return self.ways_found

    def way_callback(self, ways):
        """
        This method returns ids of  elements that contains all key-value pairs in key_values
        """

        if ways:
            for way in ways:
                if self.key_values_exist(way[1]):
                    self.ways_found.append(way[0])
                    self.way_nodes += way[2]
            #self.ways_found += [way[0] for way in ways ]
            #self.way_nodes += [way[2]]



        #print self.ways_found
        return



if __name__ == "__main__":
    filename = "../resources/MarylandAvenueNortheast.osm"
    searcher = WaySearcher(filename)
    print searcher.find_ways((("highway", None), ("name", "Maryland Avenue Northeast"))).get_ways()
