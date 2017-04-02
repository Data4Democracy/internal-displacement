from internal_displacement.model.model import Country, CountryTerm, Session
import pycountry
from sqlalchemy import create_engine
import sqlalchemy


def load_countries(session):

    for c in pycountry.countries:
        country = Country(code=c.alpha_3)
        session.add(country)
        session.commit()
        country_name = CountryTerm(term=c.name, country=country)
        session.add(country_name)
        session.commit()
        try:
            off_name = c.official_name
            if off_name != c.name:
                official_name = CountryTerm(
                    term=c.official_name, country=country)
                session.add(official_name)
                session.commit()
        except (AttributeError, sqlalchemy.exc.IntegrityError) as e:
            pass
        try:
            common_name = CountryTerm(term=c.common_name, country=country)
            session.add(common_name)
            session.commit()
        except (AttributeError, sqlalchemy.exc.IntegrityError) as e:
            pass
        session.commit()


def delete_countries(session):

    session.execute("TRUNCATE TABLE country CASCADE;")
    session.commit()
