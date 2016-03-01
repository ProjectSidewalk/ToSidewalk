from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import db
import shapefile

meta = MetaData(schema="sidewalk")
Base = declarative_base(metadata=meta)


class RegionTypeTable(Base):
    __tablename__ = "region_type"
    region_type_id = Column(Integer, primary_key=True, name="region_type_id")
    region_type = Column(String, name="region_type")

    def __repr__(self):
        return "RegionType(region_type_id=%s, region_type=%s)" % (self.region_type_id, self.region_type)

    @classmethod
    def list(cls, session):
        """
        List records of region types

        :param session:
        :return:
        """
        return [record for record in session.query(cls)]


class RegionTable(Base):
    """
    Mapping to the street_edge table.
    """
    __tablename__ = "region"
    __table_args__ = {'schema': 'sidewalk'}

    region_id = Column(Integer, primary_key=True, name="region_id")
    region_type_id = Column(Integer, ForeignKey('region_type.region_type_id'), name="region_type_id")
    description = Column(String, name="description")
    data_source = Column(String, name="data_source")
    geom = Column(Geometry("Polygon", srid=4326), name="geom")

    def __repr__(self):
        return "Region(region_id=%s, region_type_id=%s, description=%s, data_source=%s, geom=%s)" % \
               (self.region_id, self.region_type_id, self.description, self.data_source, self.geom)

    @classmethod
    def list(cls, session):
        query = session.query(cls)
        return [record for record in query]

    @classmethod
    def list_region_of_type(cls, session, type):
        region_type = session.query(RegionTypeTable).filter_by(region_type=type).first()
        return [record for record in session.query(cls).filter_by(region_type_id=region_type.region_type_id).order_by(cls.region_id)]

    @classmethod
    def add_region(cls, session, region):
        session.add(region)
        session.commit()

    @classmethod
    def add_regions(cls, session, regions):
        for region in regions:
            session.add(region)
        session.commit()


def import_dc_neighborhood(session):
    resource_file_dir = "../../resources/DCNeighborhood/Neighborhood_Composition/Neighborhood_Composition.shp"
    sf = shapefile.Reader(resource_file_dir)
    shapes = sf.shapes()

    # Insert data
    region_type_id = 2  # "neighborhood"
    data_source = "http://opendata.dc.gov/datasets/a0225495cda9411db0373a1db40a64d5_21"
    regions = []
    for i, shape in enumerate(shapes):
        polygon_string = "POLYGON((" + ",".join(["%f %f" % (coord[0], coord[1]) for coord in shape.points]) + \
                         ",%f %f" % (shape.points[0][0], shape.points[0][1]) + "))"
        regions.append(RegionTable(region_type_id=region_type_id, description="DC Neighborhood Composition", data_source=data_source, geom=polygon_string))
    RegionTable.add_regions(session, regions)


if __name__ == "__main__":
    database = db.DB("../../.settings")
    session = database.session
    for record in RegionTable.list_region_of_type(session, "neighborhood"):
        print record