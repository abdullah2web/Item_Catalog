from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Catalog, Base, MenuItem

engine = create_engine('postgresql://catalog:password@localhost/catalog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# catalog1
catalog1 = Catalog(name="Football")

session.add(catalog1)
session.commit()

menuItem1 = MenuItem(name="ball", description="The Ball is important for play football",
                        catalog=catalog1)

session.add(menuItem1)
session.commit()


# catalog2
catalog2 = Catalog(name="Basketball")

session.add(catalog2)
session.commit()

menuItem2 = MenuItem(name="Basket", description="The players will use the Basket for goals",
                        catalog=catalog2)

session.add(menuItem2)
session.commit()


print ("added menu items!")
