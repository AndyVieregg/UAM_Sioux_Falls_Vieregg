import logging

from Dao import Dao
import estimation
import processing


def biogeme_psql_out(ms_scenario, no_validation_slices, is_uam):
    logging.basicConfig(filename='Biogeme/biogemelog.log', encoding='utf-8', level=logging.INFO)

    # Estimation results
    logging.info("Entering Biogeme estimation")
    results, ll_list, est_scenario_name, est_time = estimation.estimate_mnl(ms_scenario, no_validation_slices, is_uam)
    logging.info("Done")
    processing.print_results(results, ll_list)
    results_dict = processing.results_as_dict(results, ll_list, ms_scenario, est_time)

    # PSQL output
    dao = Dao()

    dao.create_results_table(est_scenario_name)
    dao.results_to_psql(results_dict, est_scenario_name)

    return est_scenario_name


def od_comparison(ms_scenario, est_scenario):
    dao = Dao()
    dao.compare_od(ms_scenario, est_scenario)


if __name__ == '__main__':
    matsim_scenario = "uam_sp_ap_0806"
    isuam = True
    validation_slices = 10

    est_scen_name = biogeme_psql_out(matsim_scenario, validation_slices, isuam)
    #od_comparison(matsim_scenario, est_scen_name)
    #dao = Dao()
    #od_df = dao.get_od_df(matsim_scenario)

    # use OD data and estimated param values to get expected zonal OD entries per mode


    logging.info("Done")
