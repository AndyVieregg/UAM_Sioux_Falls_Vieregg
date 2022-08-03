from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert


def create_results_table(est_scen="Default"):
    engine = create_engine("postgresql+psycopg2://postgres:hainich@localhost:5433/matsim", echo=True, future=True)
    meta = MetaData()

    # Create table for estimation results
    results_table = Table(
        est_scen, meta,
        Column('ms_scenario', String),
        Column('est_time', String),
        Column('sample_size', Integer),
        Column('init_ll', Float),
        Column('final_ll', Float),
        Column('rho2', Float),
        Column('rhobar2', Float),
        Column('val_no', Integer),
        Column('val_mean_ll', Float),
        Column('val_min_ll', Float),
        Column('val_max_ll', Float),
        Column('val_ll_sd', Float),
        Column('est_asc_pt', Float),
        Column('est_asc_walk', Float),
        Column('est_asc_uam', Float),
        Column('est_b_cost', Float),
        Column('est_b_tt', Float),
        schema='est_results'
    )
    meta.create_all(engine)


def results_to_psql(results_dict, est_scen="Default"):
    engine = create_engine("postgresql+psycopg2://postgres:hainich@localhost:5433/matsim", echo=True, future=True)
    meta = MetaData()

    # Get table from scenario name
    results_table = Table(est_scen, meta, schema='est_results', autoload_with=engine)

    # Add row

    with engine.connect() as conn:
        result = conn.execute(
            insert(results_table),
            results_dict
        )
        conn.commit()


def compare_trav_times(ms_scenario):
    pass