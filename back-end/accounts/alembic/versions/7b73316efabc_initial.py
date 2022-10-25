"""initial

Revision ID: 7b73316efabc
Revises: 
Create Date: 2022-04-20 16:27:36.262079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b73316efabc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gas_counter',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('outer_base_id', sa.BigInteger(), nullable=True),
    sa.Column('setup_date', sa.DateTime(), nullable=True),
    sa.Column('in_work', sa.Boolean(), nullable=True),
    sa.Column('serial_number', sa.String(), nullable=True),
    sa.Column('data', sa.DECIMAL(precision=6, scale=3), nullable=True),
    sa.Column('old_data', sa.DECIMAL(precision=6, scale=3), nullable=True),
    sa.Column('diff', sa.DECIMAL(precision=6, scale=3), nullable=True),
    sa.Column('date_update', sa.DateTime(), nullable=True),
    sa.Column('who_last_modify', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gas_counter_id'), 'gas_counter', ['id'], unique=False)
    op.create_table('organisation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('short_name', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phones', sa.String(), nullable=True),
    sa.Column('dispatcher_phones', sa.String(), nullable=True),
    sa.Column('site', sa.String(), nullable=True),
    sa.Column('r_s', sa.String(), nullable=True),
    sa.Column('bank', sa.String(), nullable=True),
    sa.Column('bik', sa.String(), nullable=True),
    sa.Column('korr_acc', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organisation_id'), 'organisation', ['id'], unique=False)
    op.create_table('water_counter',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('outer_base_id', sa.BigInteger(), nullable=True),
    sa.Column('setup_date', sa.DateTime(), nullable=True),
    sa.Column('in_work', sa.Boolean(), nullable=True),
    sa.Column('serial_number', sa.String(), nullable=True),
    sa.Column('data', sa.DECIMAL(precision=6, scale=3), nullable=True),
    sa.Column('old_data', sa.DECIMAL(precision=6, scale=3), nullable=True),
    sa.Column('diff', sa.DECIMAL(precision=6, scale=3), nullable=True),
    sa.Column('date_update', sa.DateTime(), nullable=True),
    sa.Column('who_last_modify', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_water_counter_id'), 'water_counter', ['id'], unique=False)
    op.create_table('address',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('street', sa.String(), nullable=False),
    sa.Column('house', sa.String(), nullable=False),
    sa.Column('entrance', sa.String(), nullable=True),
    sa.Column('appartment', sa.String(), nullable=True),
    sa.Column('org_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['org_id'], ['organisation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_address_id'), 'address', ['id'], unique=False)
    op.create_table('account',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('account', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('second_name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('address_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_id'), 'account', ['id'], unique=False)
    op.create_table('account_params',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('etc', sa.String(), nullable=True),
    sa.Column('sum_square', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('living_square', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('living_quantity', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('record_living_quantity', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_params_id'), 'account_params', ['id'], unique=False)
    op.create_table('account_payment_resources_data',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('doc_date', sa.DateTime(), nullable=False),
    sa.Column('oid_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_stoch_vod', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_tpl_en_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_h_v_tepl_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_hvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_el_en', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('sod_jil', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obs_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obs_lifta', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obs_lifta_jks_36', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_rem_vdom_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_rem_vkvart_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('vodootved', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('vodootved_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('voznagr_pl_kap_rem', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gaz', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gor_voda', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gor_voda_krk_potapova1', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gorvoda_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('dop_usl', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('edv', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('kap_rem_krovli', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('kap_rem_setei', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('musoroprovod', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('nagrev_vodi', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('obrashenie_TKO', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oplata_lgot', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('otoplenie', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('peni', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('radio', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('remont_lifta', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('svet_d', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('svet_n', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('sod_obsh_priborov', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('tv', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('tepl_en_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_teploshchet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_domofona', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_domofona_spk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_vodoschet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_osmotr_vodoschet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_gaz_schet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_ip_botarov', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_ip_ivanov', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_lift', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_jks', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_rem_vkvrart_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_kod_zamka', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_met_dver', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_opu_tep_en', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_opu_hol_v', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_opu_el_en', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_prib_ucheta', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_montag_dv_sys', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('hol_voda', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('hol_voda_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('hol_voda_tepl_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_d_gaz_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_d_en_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_n_gaz_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_n_en_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('electroprovod_plit', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('electro', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_gaz_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_el_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_payment_resources_data_id'), 'account_payment_resources_data', ['id'], unique=False)
    op.create_table('account_repayment',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('doc_date', sa.DateTime(), nullable=False),
    sa.Column('oid_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_stoch_vod', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_tpl_en_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_h_v_tepl_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_hvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oid_el_en', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('sod_jil', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obs_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obs_lifta', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obs_lifta_jks_36', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_rem_vdom_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_rem_vkvart_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('vodootved', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('vodootved_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('voznagr_pl_kap_rem', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gaz', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gor_voda', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gor_voda_krk_potapova1', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('gorvoda_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('dop_usl', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('edv', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('kap_rem_krovli', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('kap_rem_setei', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('musoroprovod', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('nagrev_vodi', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('obrashenie_TKO', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('oplata_lgot', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('otoplenie', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('peni', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('radio', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('remont_lifta', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('svet_d', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('svet_n', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('sod_obsh_priborov', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('tv', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('tepl_en_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_teploshchet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_domofona', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_domofona_spk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_obsl_vodoschet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('teh_osmotr_vodoschet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_gaz_schet', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_ip_botarov', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_ip_ivanov', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_lift', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_domofona_jks', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('to_rem_vkvrart_gaz_oborud', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_kod_zamka', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_met_dver', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_opu_tep_en', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_opu_hol_v', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_opu_el_en', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_prib_ucheta', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ustanovka_montag_dv_sys', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('hol_voda', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('hol_voda_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('hol_voda_tepl_na_gvs', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_d_gaz_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_d_en_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_n_gaz_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_en_n_en_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('electroprovod_plit', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('electro', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_gaz_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('el_el_pl_pk', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_repayment_id'), 'account_repayment', ['id'], unique=False)
    op.create_table('account_summary',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('doc_date', sa.DateTime(), nullable=False),
    sa.Column('payment_sum', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('debt_start_period', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('debt', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('paying', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('last_payment_date', sa.DateTime(), nullable=False),
    sa.Column('debt_end_period', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('ending_payment', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_summary_id'), 'account_summary', ['id'], unique=False)
    op.create_table('accounts_gas_counters',
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.Column('counter_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['counter_id'], ['gas_counter.id'], ),
    sa.PrimaryKeyConstraint('account_id', 'counter_id')
    )
    op.create_table('accounts_water_counters',
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.Column('counter_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['counter_id'], ['water_counter.id'], ),
    sa.PrimaryKeyConstraint('account_id', 'counter_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts_water_counters')
    op.drop_table('accounts_gas_counters')
    op.drop_index(op.f('ix_account_summary_id'), table_name='account_summary')
    op.drop_table('account_summary')
    op.drop_index(op.f('ix_account_repayment_id'), table_name='account_repayment')
    op.drop_table('account_repayment')
    op.drop_index(op.f('ix_account_payment_resources_data_id'), table_name='account_payment_resources_data')
    op.drop_table('account_payment_resources_data')
    op.drop_index(op.f('ix_account_params_id'), table_name='account_params')
    op.drop_table('account_params')
    op.drop_index(op.f('ix_account_id'), table_name='account')
    op.drop_table('account')
    op.drop_index(op.f('ix_address_id'), table_name='address')
    op.drop_table('address')
    op.drop_index(op.f('ix_water_counter_id'), table_name='water_counter')
    op.drop_table('water_counter')
    op.drop_index(op.f('ix_organisation_id'), table_name='organisation')
    op.drop_table('organisation')
    op.drop_index(op.f('ix_gas_counter_id'), table_name='gas_counter')
    op.drop_table('gas_counter')
    # ### end Alembic commands ###