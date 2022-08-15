from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, select
import pandas as pd


class Dao:

    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:hainich@localhost:5433/matsim",
                                    echo=True, future=True)
        self.meta = MetaData()
        self.ms_scenarios = {'non_uam_bl', 'uam_bl', 'uam_sp_test'}

    def get_ms_scenario_schema_name(self, ms_scenario):
        for name in self.ms_scenarios:
            if ms_scenario.startswith(name):
                return name

        raise RuntimeError('Scenario name not found in list of tables')

    def create_results_table(self, est_scen="Default"):

        # Create table for estimation results
        results_table = Table(
            est_scen, self.meta,
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
        self.meta.create_all(self.engine)

    def results_to_psql(self, results_dict, est_scen="Default"):
        engine = self.engine
        meta = self.meta

        # Get table from scenario name
        results_table = Table(est_scen, meta, schema='est_results', autoload_with=engine)

        # Add row

        with engine.connect() as conn:
            result = conn.execute(
                insert(results_table),
                results_dict
            )
            conn.commit()

    def get_od_df(self, ms_scenario):
        schema_name = self.get_ms_scenario_schema_name(ms_scenario)

        od_table = Table('od', self.meta, schema=schema_name, autoload_with=self.engine)

        is_uam = False
        if 'num_uam' in od_table.c.keys():
            is_uam = True

        with self.engine.connect() as conn:
            df = pd.read_sql(select(od_table), conn, index_col=od_table.c.relation)

        return df

    def compare_od(self, ms_scenario, est_scenario):
        # Get OD table corresponding to the MATSim scenario

        schema_name = self.get_ms_scenario_schema_name(ms_scenario)
        od_table = Table('od', self.meta, schema=schema_name, autoload_with=self.engine)
        est_table = Table(est_scenario, self.meta, schema='est_results', autoload_with=self.engine)

        is_uam = False
        if 'num_uam' in od_table.c.keys():
            is_uam = True

        # Create OD comparison table
        od_comp_table = Table('od_comp', self.meta,
                              Column('relation', String),
                              Column('origin', Integer),
                              Column('dest', Integer),
                              Column('num_trips', Integer),
                              Column('num_car', Integer),
                              Column('num_pt', Integer),
                              Column('num_walk', Integer),
                              Column('num_uam', Integer),
                              Column('num_car_' + est_scenario, Integer),
                              Column('num_pt_' + est_scenario, Integer),
                              Column('num_walk_' + est_scenario, Integer),
                              Column('num_uam_' + est_scenario, Integer),
                              schema=schema_name)
        self.meta.create_all(self.engine)

        # Get and commit new OD rows
        with self.engine.connect() as conn:
            for o in range(1, 25):
                for d in range(1, 25):
                    od_row = {}

                    # get O-D data from PSQL
                    relation = str(o) + '-' + str(d)
                    od_res = conn.execute(select(od_table.c.num_trips,
                                                 od_table.c.num_car,
                                                 od_table.c.num_pt,
                                                 od_table.c.num_walk
                                                 ).where(od_table.c.relation == relation)).first()

                    # create dict for row of O-D comparison table
                    od_row.update({'relation': relation, 'origin': o, 'dest': d,
                                   'num_trips': od_res[0], 'num_car': od_res[1], 'num_pt': od_res[2],
                                   'num_walk': od_res[3]})

                    # UAM time treated separately
                    if is_uam:
                        od_row.update({'num_uam': conn.execute(select(od_table.c.num_trips).where(
                            od_table.c.relation == relation)).first()})

                    # Get estimated O-D data from PSQL

                    od_est = conn.execute(
                        select(est_table.c.ms_scenario)
                        .where(est_table.c.ms_scenario == ms_scenario).order_by(est_table.c.est_time)
                    ).first()
                    print(od_est)
        conn.commit()
