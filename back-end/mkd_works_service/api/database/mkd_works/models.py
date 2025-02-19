import uuid
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Text, DateTime, select, DECIMAL, Numeric
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import AssociationProxy
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
    dirname_who_what = Column(String, nullable=True)
    dirsurname_who_what = Column(String, nullable=True)
    dirsecondname_who_what = Column(String, nullable=True)

    houses = relationship("Houses", back_populates="companies")

class Houses(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    house_square = Column(Numeric, nullable=True)
    director_fio = Column(String, nullable=True)
    director_appartment = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete="SET NULL"), nullable=True)

    # заменено на select вешает запрос 
    companies = relationship('Companies', back_populates='houses', lazy='joined')
    actfiles = relationship('Actfiles', back_populates='houses', lazy='select')
    smetafiles = relationship('Smetafiles', back_populates='houses', lazy='select')
    techfiles = relationship('Techfiles', back_populates='houses', lazy='select')
    acts = relationship('Acts', back_populates='houses', lazy='select')
    yearactfiles = relationship('YearActfiles', back_populates='houses', lazy='select')
    photofilesdoneworks = relationship('PhotoFilesDoneWorks', back_populates='houses', lazy='select')


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
    notes = Column(String, nullable=True)
    act_custom_period = Column(String, nullable=True)

    acts = relationship("Acts", back_populates="mainworks_details", lazy='joined', viewonly=True)
    mainworks = relationship('Mainworks', back_populates='acts_details', lazy='joined', viewonly=True)


class Acthassubworks(Base):
    __tablename__ = "acthassubworks"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    subwork_id = Column(Integer, ForeignKey("subworks.id"), primary_key=True, nullable=False)
    sum = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    unitcost = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    act_custom_period = Column(String, nullable=True)

    acts = relationship("Acts", back_populates="subworks_details", lazy='joined', viewonly=True)
    subworks = relationship('Subworks', back_populates='acts_details', lazy='joined', viewonly=True)


class Acthasfixworks(Base):
    __tablename__ = "acthasfixworks"

    act_id = Column(Integer, ForeignKey("acts.id"), primary_key=True, nullable=False)
    fixwork_id = Column(Integer, ForeignKey("fixworks.id"), primary_key=True, nullable=False)
    sum = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    unitcost = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    act_custom_period = Column(String, nullable=True)

    acts = relationship("Acts", back_populates="fixworks_details", lazy='joined', viewonly=True)
    fixworks = relationship('Fixworks', back_populates='acts_details', lazy='joined', viewonly=True)


class Mainworks(Base):
    __tablename__ = "mainworks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    work = Column(String, nullable=False)
    workType = Column(String, nullable=False)
    companyWorkType= Column(String, nullable=True)
    numsprav = Column(String, nullable=True)
    period = Column(String, nullable=True)

    subworks = relationship('Subworks', back_populates='mainworks', lazy='select')
    fixworks = relationship('Fixworks', back_populates='mainworks', lazy='select')
    acts = relationship('Acts', secondary='acthasmainworks', back_populates='mainworks', lazy='select')
    acts_details = relationship("Acthasmainworks", back_populates="mainworks", lazy='joined', viewonly=True)
    
    @hybrid_property
    def sum(self):
        return self.acts_details[0].sum if self.acts_details else None

    #@property
    @hybrid_property
    def quantity(self):
        return self.acts_details[0].quantity if self.acts_details else None

    #@property
    @hybrid_property
    def unitcost(self):
        return self.acts_details[0].unitcost if self.acts_details else None
    
    @hybrid_property
    def notes(self):
        return self.acts_details[0].notes if self.acts_details else None
    
    @hybrid_property
    def act_custom_period(self):
        return self.acts_details[0].act_custom_period if self.acts_details else None
    


class Subworks(Base):
    __tablename__ = "subworks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    work = Column(String, nullable=False)
    ext_works = Column(String, nullable=True)
    workType = Column(String, nullable=False)
    companyWorkType= Column(String, nullable=True)
    period = Column(String, nullable=True)
    base = Column(String, nullable=True)
    numsprav = Column(String, nullable=True)
    mainwork_id = Column(Integer, ForeignKey('mainworks.id'), nullable=True)

    mainworks = relationship('Mainworks', back_populates='subworks', lazy='joined')
    acts = relationship('Acts', secondary='acthassubworks', back_populates='subworks', lazy='joined', viewonly=True)
    acts_details = relationship("Acthassubworks", back_populates="subworks", lazy='joined', viewonly=True)
    """sum = AssociationProxy('acts_details', 'sum', creator=lambda values: values[0] if values else None)
    quantity = AssociationProxy('acts_details', 'quantity', creator=lambda values: values[0] if values else None)
    unitcost = AssociationProxy('acts_details', 'unitcost', creator=lambda values: values[0] if values else None)"""
    #@property
    @hybrid_property
    def sum(self):
        return self.acts_details[0].sum if self.acts_details else None

    #@property
    @hybrid_property
    def quantity(self):
        return self.acts_details[0].quantity if self.acts_details else None

    #@property
    @hybrid_property
    def unitcost(self):
        return self.acts_details[0].unitcost if self.acts_details else None
    
    @hybrid_property
    def notes(self):
        return self.acts_details[0].notes if self.acts_details else None
    
    @hybrid_property
    def act_custom_period(self):
        return self.acts_details[0].act_custom_period if self.acts_details else None

class Fixworks(Base):
    __tablename__ = "fixworks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    work = Column(String, nullable=False)
    ext_works = Column(String, nullable=True)
    workType = Column(String, nullable=False)
    companyWorkType= Column(String, nullable=True)
    period = Column(String, nullable=True)
    base = Column(String, nullable=True)
    numsprav = Column(String, nullable=True)
    mainwork_id = Column(Integer, ForeignKey('mainworks.id'), nullable=True)

    mainworks = relationship('Mainworks', back_populates='fixworks', lazy='select')
    acts = relationship('Acts', secondary='acthasfixworks', back_populates='fixworks', lazy='select', viewonly=True)
    acts_details = relationship("Acthasfixworks", back_populates="fixworks", lazy='joined', viewonly=True)

    #@property
    @hybrid_property
    def sum(self):
        return self.acts_details[0].sum if self.acts_details else None

    #@property
    @hybrid_property
    def quantity(self):
        return self.acts_details[0].quantity if self.acts_details else None

    #@property
    @hybrid_property
    def unitcost(self):
        return self.acts_details[0].unitcost if self.acts_details else None
    
    @hybrid_property
    def notes(self):
        return self.acts_details[0].notes if self.acts_details else None
    
    @hybrid_property
    def act_custom_period(self):
        return self.acts_details[0].act_custom_period if self.acts_details else None


class Actfiles(Base):
    __tablename__ = "actfiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    url = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())

    houses = relationship('Houses', back_populates='actfiles', lazy='joined')
    acts = relationship('Acts', secondary='actshasactfiles', primaryjoin="Acts.id == Actshasactfiles.act_id",
    secondaryjoin="Actfiles.uuid == Actshasactfiles.actfile_uuid", back_populates='actfiles', lazy='joined')


class Smetafiles(Base):
    __tablename__ = "smetafiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    url = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())

    houses = relationship('Houses', back_populates='smetafiles', lazy='joined')
    acts = relationship('Acts', secondary='actshassmetafiles', back_populates='smetafiles', primaryjoin="Acts.id == Actshassmetafiles.act_id",
    secondaryjoin="Smetafiles.uuid == Actshassmetafiles.smetafile_uuid", lazy='joined')


class Techfiles(Base):
    __tablename__ = "techfiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    url = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)

    houses = relationship('Houses', back_populates='techfiles', lazy='joined')



class Acts(Base):
    __tablename__ = "acts"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    num = Column(String, nullable=True)
    all_sum = Column(String, nullable=False)
    month_year_works = Column(DateTime, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    unit_cost = Column(String, nullable=True)
    work_square = Column(String, nullable=True)
    director = Column(String, nullable=True)
    director_appartment = Column(String, nullable=True)

    houses = relationship('Houses', back_populates='acts', lazy='joined')
    mainworks = relationship(
        'Mainworks', secondary='acthasmainworks', primaryjoin="Acts.id == Acthasmainworks.act_id",  secondaryjoin="Mainworks.id == Acthasmainworks.mainwork_id", 
        back_populates='acts', lazy='joined', overlaps="acts"
    )

    mainworks_details = relationship("Acthasmainworks", back_populates="acts", lazy='joined', viewonly=True)

    subworks = relationship(
        'Subworks', secondary='acthassubworks', primaryjoin="Acts.id == Acthassubworks.act_id",  secondaryjoin="Subworks.id == Acthassubworks.subwork_id", 
        back_populates='acts', lazy='joined', overlaps="acts"
    )

    subworks_details = relationship("Acthassubworks", back_populates="acts", lazy='joined', viewonly=True)


    fixworks = relationship(
        'Fixworks', secondary='acthasfixworks', back_populates='acts', lazy='joined', primaryjoin="Acts.id == Acthasfixworks.act_id", 
        secondaryjoin="Fixworks.id == Acthasfixworks.fixwork_id", overlaps='acts'
    )

    fixworks_details = relationship("Acthasfixworks", back_populates="acts", lazy='joined', viewonly=True)

    actfiles = relationship(
        'Actfiles', secondary='actshasactfiles', back_populates='acts', lazy='joined', order_by="desc(Actfiles.date_upload)"
    )

    smetafiles = relationship(
        'Smetafiles', secondary='actshassmetafiles', back_populates='acts', lazy='joined', order_by="desc(Smetafiles.date_upload)"
    )

    photofilesdoneworks = relationship('PhotoFilesDoneWorks', back_populates='acts', lazy='select')


class YearActfiles(Base):
    __tablename__ = "yearactfiles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    year = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    url = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())

    houses = relationship('Houses', back_populates='yearactfiles', lazy='joined')

class BGTasks(Base):
    __tablename__="bg_tasks"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, nullable=False)
    start_datetime = Column(DateTime(timezone=True), server_default=func.now())
    end_datetime = Column(DateTime, nullable=True)
    type = Column(String, nullable=True)
    percent = Column(String, nullable=True)

class PhotoFilesDoneWorks(Base):
    __tablename__="photofilesdoneworks"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    num = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    extention = Column(String, nullable=False)
    url = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=False)
    filetype = Column(String, nullable=True)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    act_id = Column(Integer, ForeignKey("acts.id"), nullable=False)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())

    houses = relationship('Houses', back_populates='photofilesdoneworks', lazy='joined')
    acts = relationship('Acts', back_populates='photofilesdoneworks', lazy='joined')



