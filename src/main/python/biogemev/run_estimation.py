import estimation
import processing
import logging


def run():
    logging.basicConfig(filename='Biogeme/biogemelog.log', encoding='utf-8', level=logging.INFO)

    logging.info("Entering Biogeme estimation")
    results, ll_list, scenario_name = estimation.estimate_mnl("non_uam_bl_0719")
    logging.info("Done")
    processing.print_results(results, ll_list)


if __name__ == '__main__':
    run()
    logging.info("Done")
