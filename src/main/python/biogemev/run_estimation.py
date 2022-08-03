import logging

import dao
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
    dao.create_results_table(est_scenario_name)
    dao.results_to_psql(results_dict, est_scenario_name)


def tt_comparison(ms_scenario):
    dao.compare_trav_times(ms_scenario)


if __name__ == '__main__':
    ms_scenario = "uam_sp_test_0801"
    is_uam = True
    no_validation_slices = 10

    biogeme_psql_out(ms_scenario, is_uam, no_validation_slices)

    logging.info("Done")
