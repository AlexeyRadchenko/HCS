import uuid
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Text, DateTime, select, DECIMAL
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()

class Organisation(Base):
    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phones = Column(String, nullable=True)
    dispatcher_phones = Column(String, nullable=True)
    site = Column(String, nullable=True)
    r_s = Column(String, nullable=True)
    bank = Column(String, nullable=True)
    bik = Column(String, nullable=True)
    inn = Column(String, nullable=True)
    kpp = Column(String, nullable=True)
    qr_short_name = Column(String, nullable=True)
    korr_acc = Column(String, nullable=True)

    """clients = relationship(
        'ContactsClients', secondary='clients_addresses', back_populates='addresses', lazy='dynamic'
    )"""
    #clients = relationship('ContactsClientsAddresses', back_populates='address')
    #address_extend = relationship('ContactsClientsAddresses', backref='addresses', lazy='joined')

class Address(Base):
    __tablename__ = "address"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    entrance = Column(String, nullable=True)
    appartment = Column(String, nullable=True)
    org_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    account = relationship("Account", back_populates="address")
    

class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    account = Column(String, nullable=False)
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)
    address = relationship('Address', back_populates='account', lazy='joined')
    electric_counters = relationship('ElectricCounter', secondary='accounts_electric_counters', lazy='joined')
    water_counters = relationship('WaterCounter', secondary='accounts_water_counters', lazy='joined')
    gas_counters = relationship('GasCounter', secondary='accounts_gas_counters', lazy='joined')
    account_params = relationship('AccountParams', back_populates='account', lazy='joined', uselist=False) 
    account_summary = relationship('AccountSummary', back_populates='account', lazy='joined', uselist=False)

class ElectricCounter(Base):
    __tablename__ = "electric_counter"
    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    outer_base_id = Column(BigInteger, nullable=True)
    setup_date = Column(DateTime, nullable=True)
    in_work = Column(Boolean, default=True)
    type = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    simple_data = Column(Integer, nullable=True)
    day_data = Column(Integer, nullable=True)
    night_data = Column(Integer, nullable=True)
    old_simple_data = Column(Integer, nullable=True)
    old_day_data = Column(Integer, nullable=True)
    old_night_data = Column(Integer, nullable=True)
    simple_diff = Column(Integer, nullable=True)
    day_diff = Column(Integer, nullable=True)
    night_diff = Column(Integer, nullable=True)
    date_update = Column(DateTime, nullable=True)
    last_date_update = Column(DateTime, nullable=True)
    who_last_modify = Column(String, nullable=True)

class WaterCounter(Base):
    __tablename__ = "water_counter"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    outer_base_id = Column(BigInteger, nullable=True)
    setup_date = Column(DateTime, nullable=True)
    in_work = Column(Boolean, default=True)
    type = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    data = Column(DECIMAL(precision=6, scale=3), nullable=True)
    old_data = Column(DECIMAL(precision=6, scale=3), nullable=True)
    diff = Column(DECIMAL(precision=6, scale=3), nullable=True)
    date_update = Column(DateTime, nullable=True)
    last_date_update = Column(DateTime, nullable=True)
    who_last_modify = Column(String, nullable=True)

class AccountsElectricCounters(Base):
    __tablename__ = "accounts_electric_counters"

    account_id = Column(BigInteger, ForeignKey('account.id'), primary_key=True)
    counter_id = Column(BigInteger, ForeignKey('electric_counter.id'), primary_key=True)    

class AccountsWaterCounters(Base):
    __tablename__ = "accounts_water_counters"

    account_id = Column(BigInteger, ForeignKey('account.id'), primary_key=True)
    counter_id = Column(BigInteger, ForeignKey('water_counter.id'), primary_key=True)

class GasCounter(Base):
    __tablename__ = "gas_counter"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    outer_base_id = Column(BigInteger, nullable=True)
    setup_date = Column(DateTime, nullable=True)
    in_work = Column(Boolean, default=True)
    serial_number = Column(String, nullable=True)
    data = Column(DECIMAL(precision=6, scale=3), nullable=True)
    old_data = Column(DECIMAL(precision=6, scale=3), nullable=True)
    diff = Column(DECIMAL(precision=6, scale=3), nullable=True)
    date_update = Column(DateTime, nullable=True)
    last_date_update = Column(DateTime, nullable=True)
    who_last_modify = Column(String, nullable=True)

class AccountsGasCounters(Base):
    __tablename__ = "accounts_gas_counters"

    account_id = Column(BigInteger, ForeignKey('account.id'), primary_key=True)
    counter_id = Column(BigInteger, ForeignKey('gas_counter.id'), primary_key=True)

class AccountParams(Base):
    __tablename__ = "account_params"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    etc = Column(String, nullable=True)
    sum_square = Column(DECIMAL(12,2), nullable=True)
    living_square = Column(DECIMAL(12,2), nullable=True)
    living_quantity = Column(DECIMAL(12,2), nullable=True)
    record_living_quantity = Column(DECIMAL(12,2), nullable=True)
    account_id = Column(BigInteger, ForeignKey('account.id'), nullable = False)
    account = relationship("Account", back_populates="account_params")

class AccountSummary(Base):
    __tablename__ = "account_summary"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    doc_date = Column(DateTime, nullable=False)
    payment_sum = Column(DECIMAL(12,2), nullable=True)
    debt_start_period = Column(DECIMAL(12,2), nullable=True)
    debt = Column(DECIMAL(12,2), nullable=True)
    paying = Column(DECIMAL(12,2), nullable=True)
    last_payment_date = Column(DateTime, nullable=False)
    debt_end_period = Column(DECIMAL(12,2), nullable=True)
    ending_payment = Column(DECIMAL(12,2), nullable=True)
    account_id = Column(BigInteger, ForeignKey('account.id'), nullable = False)
    account = relationship("Account", back_populates="account_summary")

class AccountPaymentResourcesData(Base):
    __tablename__ = "account_payment_resources_data"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    doc_date = Column(DateTime, nullable=False)
    oid_gvs = Column(DECIMAL(12,2), nullable=True)
    oid_stoch_vod = Column(DECIMAL(12,2), nullable=True)
    oid_tpl_en_na_gvs = Column(DECIMAL(12,2), nullable=True)
    oid_h_v_tepl_na_gvs = Column(DECIMAL(12,2), nullable=True)
    oid_hvs = Column(DECIMAL(12,2), nullable=True)
    oid_el_en = Column(DECIMAL(12,2), nullable=True)
    sod_jil = Column(DECIMAL(12,2), nullable=True)
    teh_obs_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    teh_obs_lifta = Column(DECIMAL(12,2), nullable=True)
    teh_obs_lifta_jks_36 = Column(DECIMAL(12,2), nullable=True)
    to_rem_vdom_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    to_rem_vkvart_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    vodootved = Column(DECIMAL(12,2), nullable=True)
    vodootved_pk = Column(DECIMAL(12,2), nullable=True)
    voznagr_pl_kap_rem = Column(DECIMAL(12,2), nullable=True)
    gaz = Column(DECIMAL(12,2), nullable=True)
    gor_voda = Column(DECIMAL(12,2), nullable=True)
    gor_voda_krk_potapova1 = Column(DECIMAL(12,2), nullable=True)
    gorvoda_pk = Column(DECIMAL(12,2), nullable=True)
    dop_usl = Column(DECIMAL(12,2), nullable=True)
    edv = Column(DECIMAL(12,2), nullable=True)
    kap_rem_krovli = Column(DECIMAL(12,2), nullable=True)
    kap_rem_setei = Column(DECIMAL(12,2), nullable=True)
    musoroprovod = Column(DECIMAL(12,2), nullable=True)
    nagrev_vodi = Column(DECIMAL(12,2), nullable=True)
    obrashenie_TKO = Column(DECIMAL(12,2), nullable=True)
    oplata_lgot = Column(DECIMAL(12,2), nullable=True)
    otoplenie = Column(DECIMAL(12,2), nullable=True)
    peni = Column(DECIMAL(12,2), nullable=True)
    radio = Column(DECIMAL(12,2), nullable=True)
    remont_lifta = Column(DECIMAL(12,2), nullable=True)
    svet_d = Column(DECIMAL(12,2), nullable=True)
    svet_n = Column(DECIMAL(12,2), nullable=True)
    sod_obsh_priborov = Column(DECIMAL(12,2), nullable=True)
    tv = Column(DECIMAL(12,2), nullable=True)
    tepl_en_na_gvs = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_teploshchet = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_domofona = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_domofona_spk = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_vodoschet = Column(DECIMAL(12,2), nullable=True)
    teh_osmotr_vodoschet = Column(DECIMAL(12,2), nullable=True)
    to_gaz_schet = Column(DECIMAL(12,2), nullable=True)
    to_domofona_ip_botarov = Column(DECIMAL(12,2), nullable=True)
    to_domofona_ip_ivanov = Column(DECIMAL(12,2), nullable=True)
    to_domofona_lift = Column(DECIMAL(12,2), nullable=True)
    to_domofona_jks = Column(DECIMAL(12,2), nullable=True)
    to_rem_vkvrart_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    ustanovka_kod_zamka = Column(DECIMAL(12,2), nullable=True)
    ustanovka_met_dver = Column(DECIMAL(12,2), nullable=True)
    ustanovka_opu_tep_en = Column(DECIMAL(12,2), nullable=True)
    ustanovka_opu_hol_v = Column(DECIMAL(12,2), nullable=True)
    ustanovka_opu_el_en = Column(DECIMAL(12,2), nullable=True)
    ustanovka_prib_ucheta = Column(DECIMAL(12,2), nullable=True)
    ustanovka_montag_dv_sys = Column(DECIMAL(12,2), nullable=True)
    hol_voda = Column(DECIMAL(12,2), nullable=True)
    hol_voda_pk = Column(DECIMAL(12,2), nullable=True)
    hol_voda_tepl_na_gvs = Column(DECIMAL(12,2), nullable=True)
    el_en_d_gaz_pl_pk = Column(DECIMAL(12,2), nullable=True)
    el_en_d_en_pl_pk = Column(DECIMAL(12,2), nullable=True)   
    el_en_n_gaz_pl_pk = Column(DECIMAL(12,2), nullable=True)
    el_en_n_en_pl_pk = Column(DECIMAL(12,2), nullable=True)
    electroprovod_plit = Column(DECIMAL(12,2), nullable=True)
    electro = Column(DECIMAL(12,2), nullable=True)
    el_gaz_pl_pk = Column(DECIMAL(12,2), nullable=True)
    el_el_pl_pk = Column(DECIMAL(12,2), nullable=True)
    account_id = Column(BigInteger, ForeignKey('account.id'), nullable = False)

class AccountRePayment(Base):
    __tablename__ = "account_repayment"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    doc_date = Column(DateTime, nullable=False)
    oid_gvs = Column(DECIMAL(12,2), nullable=True)
    oid_stoch_vod = Column(DECIMAL(12,2), nullable=True)
    oid_tpl_en_na_gvs = Column(DECIMAL(12,2), nullable=True)
    oid_h_v_tepl_na_gvs = Column(DECIMAL(12,2), nullable=True)
    oid_hvs = Column(DECIMAL(12,2), nullable=True)
    oid_el_en = Column(DECIMAL(12,2), nullable=True)
    sod_jil = Column(DECIMAL(12,2), nullable=True)
    teh_obs_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    teh_obs_lifta = Column(DECIMAL(12,2), nullable=True)
    teh_obs_lifta_jks_36 = Column(DECIMAL(12,2), nullable=True)
    to_rem_vdom_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    to_rem_vkvart_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    vodootved = Column(DECIMAL(12,2), nullable=True)
    vodootved_pk = Column(DECIMAL(12,2), nullable=True)
    voznagr_pl_kap_rem = Column(DECIMAL(12,2), nullable=True)
    gaz = Column(DECIMAL(12,2), nullable=True)
    gor_voda = Column(DECIMAL(12,2), nullable=True)
    gor_voda_krk_potapova1 = Column(DECIMAL(12,2), nullable=True)
    gorvoda_pk = Column(DECIMAL(12,2), nullable=True)
    dop_usl = Column(DECIMAL(12,2), nullable=True)
    edv = Column(DECIMAL(12,2), nullable=True)
    kap_rem_krovli = Column(DECIMAL(12,2), nullable=True)
    kap_rem_setei = Column(DECIMAL(12,2), nullable=True)
    musoroprovod = Column(DECIMAL(12,2), nullable=True)
    nagrev_vodi = Column(DECIMAL(12,2), nullable=True)
    obrashenie_TKO = Column(DECIMAL(12,2), nullable=True)
    oplata_lgot = Column(DECIMAL(12,2), nullable=True)
    otoplenie = Column(DECIMAL(12,2), nullable=True)
    peni = Column(DECIMAL(12,2), nullable=True)
    radio = Column(DECIMAL(12,2), nullable=True)
    remont_lifta = Column(DECIMAL(12,2), nullable=True)
    svet_d = Column(DECIMAL(12,2), nullable=True)
    svet_n = Column(DECIMAL(12,2), nullable=True)
    sod_obsh_priborov = Column(DECIMAL(12,2), nullable=True)
    tv = Column(DECIMAL(12,2), nullable=True)
    tepl_en_na_gvs = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_teploshchet = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_domofona = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_domofona_spk = Column(DECIMAL(12,2), nullable=True)
    teh_obsl_vodoschet = Column(DECIMAL(12,2), nullable=True)
    teh_osmotr_vodoschet = Column(DECIMAL(12,2), nullable=True)
    to_gaz_schet = Column(DECIMAL(12,2), nullable=True)
    to_domofona_ip_botarov = Column(DECIMAL(12,2), nullable=True)
    to_domofona_ip_ivanov = Column(DECIMAL(12,2), nullable=True)
    to_domofona_lift = Column(DECIMAL(12,2), nullable=True)
    to_domofona_jks = Column(DECIMAL(12,2), nullable=True)
    to_rem_vkvrart_gaz_oborud = Column(DECIMAL(12,2), nullable=True)
    ustanovka_kod_zamka = Column(DECIMAL(12,2), nullable=True)
    ustanovka_met_dver = Column(DECIMAL(12,2), nullable=True)
    ustanovka_opu_tep_en = Column(DECIMAL(12,2), nullable=True)
    ustanovka_opu_hol_v = Column(DECIMAL(12,2), nullable=True)
    ustanovka_opu_el_en = Column(DECIMAL(12,2), nullable=True)
    ustanovka_prib_ucheta = Column(DECIMAL(12,2), nullable=True)
    ustanovka_montag_dv_sys = Column(DECIMAL(12,2), nullable=True)
    hol_voda = Column(DECIMAL(12,2), nullable=True)
    hol_voda_pk = Column(DECIMAL(12,2), nullable=True)
    hol_voda_tepl_na_gvs = Column(DECIMAL(12,2), nullable=True)
    el_en_d_gaz_pl_pk = Column(DECIMAL(12,2), nullable=True)
    el_en_d_en_pl_pk = Column(DECIMAL(12,2), nullable=True)   
    el_en_n_gaz_pl_pk = Column(DECIMAL(12,2), nullable=True)
    el_en_n_en_pl_pk = Column(DECIMAL(12,2), nullable=True)
    electroprovod_plit = Column(DECIMAL(12,2), nullable=True)
    electro = Column(DECIMAL(12,2), nullable=True)
    el_gaz_pl_pk = Column(DECIMAL(12,2), nullable=True)
    el_el_pl_pk = Column(DECIMAL(12,2), nullable=True)
    account_id = Column(BigInteger, ForeignKey('account.id'), nullable = False)





