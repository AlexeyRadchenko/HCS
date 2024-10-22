import uuid
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Text, DateTime, select, DECIMAL
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()


class Companies(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    dirname = Column(String, nullable=True)
    dirsurname = Column(String, nullable=True)
    dirsecondname = Column(String, nullable=True)

    houses = relationship("Houses", back_populates="companies")

class Houses(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    director = Column(String, nullable=True)
    director_appartment = Column(String, nullable=True)

    companies = relationship('Companies', back_populates='houses', lazy='joined')
    actfiles = relationship('Actfiles', back_populates='houses', lazy='joined')
    smetafiles = relationship('Smetafiles', back_populates='houses', lazy='joined')
    techfiles = relationship('Techfiles', back_populates='houses', lazy='joined')
    acts = relationship('Acts', back_populates='houses', lazy='joined')


class Actshasactfiles(Base):
    __tablename__ = "actshasactfiles"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    actfile_uuid = Column(UUID(as_uuid=True), ForeignKey("actfiles.uuid"), primary_key=True, nullable=False)


class Actshassmetafiles(Base):
    __tablename__ = "actshassmetafiles"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    smetafile_uuid = Column(UUID(as_uuid=True), ForeignKey("smetafiles.uuid"), primary_key=True, nullable=False)


class Acthasmainworks(Base):
    __tablename__ = "acthasmainworks"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    mainwork_id = Column(Integer, ForeignKey("mainworks.id"), primary_key=True, nullable=False)
    sum = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    unitcost = Column(String, nullable=True)


class Acthassubworks(Base):
    __tablename__ = "acthassubworks"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    subwork_id = Column(Integer, ForeignKey("subworks.id"), primary_key=True, nullable=False)
    sum = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    unitcost = Column(String, nullable=True)


class Acthasfixworks(Base):
    __tablename__ = "acthasfixworks"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    fixwork_id = Column(Integer, ForeignKey("fixworks.id"), primary_key=True, nullable=False)
    sum = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    unitcost = Column(String, nullable=True)


class Mainworks(Base):
    __tablename__ = "mainworks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    work = Column(String, nullable=False)
    workType = Column(String, nullable=False)
    companyWorkType= Column(String, nullable=False)

    subworks = relationship('Subworks', back_populates='mainworks', lazy='joined')
    fixworks = relationship('Fixworks', back_populates='mainworks', lazy='joined')
    acts = relationship('Acts', secondary='acthasmainworks', back_populates='mainworks', lazy='dynamic')
    


class Subworks(Base):
    __tablename__ = "subworks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    work = Column(String, nullable=False)
    workType = Column(String, nullable=False)
    companyWorkType= Column(String, nullable=False)
    period = Column(String, nullable=False)
    base = Column(String, nullable=False)
    mainwork_id = Column(Integer, ForeignKey('mainworks.id'), nullable=True)

    mainworks = relationship('Mainworks', back_populates='subworks', lazy='joined')
    acts = relationship('Acts', secondary='acthassubworks', back_populates='subworks', lazy='dynamic')


class Fixworks(Base):
    __tablename__ = "fixworks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    work = Column(String, nullable=False)
    workType = Column(String, nullable=False)
    companyWorkType= Column(String, nullable=False)
    period = Column(String, nullable=False)
    base = Column(String, nullable=False)
    mainwork_id = Column(Integer, ForeignKey('mainworks.id'), nullable=True)

    mainworks = relationship('Mainworks', back_populates='fixworks', lazy='joined')
    acts = relationship('Acts', secondary='acthasfixworks', back_populates='fixworks', lazy='dynamic')


class Actfiles(Base):
    __tablename__ = "actfiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)

    houses = relationship('Houses', back_populates='actfiles', lazy='joined')
    acts = relationship('Acts', secondary='actshasactfiles', back_populates='actfiles', lazy='dynamic')


class Smetafiles(Base):
    __tablename__ = "smetafiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)

    houses = relationship('Houses', back_populates='smetafiles', lazy='joined')
    acts = relationship('Acts', secondary='actshassmetafiles', back_populates='smetafiles', lazy='dynamic')


class Techfiles(Base):
    __tablename__ = "techfiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)

    houses = relationship('Houses', back_populates='techfiles', lazy='joined')



class Acts(Base):
    __tablename__ = "acts"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    num = Column(String, nullable=True)
    all_sum = Column(String, nullable=True)
    month_year_works = Column(DateTime, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)

    houses = relationship('Houses', back_populates='acts', lazy='joined')
    mainworks = relationship(
        'Mainworks', secondary='acthasmainworks', back_populates='acts', lazy='dynamic'
    )

    subworks = relationship(
        'Subworks', secondary='acthassubworks', back_populates='acts', lazy='dynamic'
    )


    fixworks = relationship(
        'Fixworks', secondary='acthasfixworks', back_populates='acts', lazy='dynamic'
    )

    actfiles = relationship(
        'Actfiles', secondary='actshasactfiles', back_populates='acts', lazy='dynamic'
    )

    smetafiles = relationship(
        'Smetafiles', secondary='actshassmetafiles', back_populates='acts', lazy='dynamic'
    )

   
