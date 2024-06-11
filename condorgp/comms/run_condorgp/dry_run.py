from condorgp.gp.gp_control import GpControl
import sys, os
import logging, time

# def main():
#     cgp = GpControl()
#     cgp.main()
    
def undertake_cgp_run():
    start_time = time.time()

    gpc = GpControl()
    gpc.verbose = 1

    gpc.use_adfs = 1
    if gpc.use_adfs:
        pset_used = 'naut_pset_03_strategy' # 'naut_pset_03_strategy'
        # 'naut_pset_02_adf' # 'test_adf_symbreg_pset' # 'test_pset5b'
    else:
        pset_used = 'naut_pset_01' #  'test_pset5b'
    eval_used = 'eval_nautilus' # evalSymbRegTest

    p = 1
    g = 1
    cp_base = "first_strat"
    cp_freq = g+1
    gpc.set_gp_n_cp(freq=cp_freq, cp_file=cp_base+"")

    # gpc.select_gp_provider_for_ADFs() # call to use ADFs but not checkpoints
    gpc.setup_gp(pset_spec=pset_used, pop_size=p, no_gens=g)
    gpc.set_test_evaluator(eval_used)

    gpc.run_backtest = 0
    gpc.inject_strategy = 1 # set to 1, this selects naut_06_gp_strategy

    gpc.run_gp()

    # tidy up
    gpc.util.tidy_cp_files(cp_base)

    if gpc.verbose:
        logging.info(' deap __ Hall of fame:')
        for x, individual in enumerate(gpc.gp.hof):
            printed_ind = [str(tree) for tree in gpc.gp.hof.items[x]]
            logging.info(f" deap generated individual: {printed_ind}")

    logging.debug(f"GpControl run, evaluator: {eval_used}, pset: {pset_used}")

    best = gpc.gp.hof.items[0]
    printed_ind = [str(tree) for tree in best]
    logging.info(f" Evolution run, best individual: \n\
        {printed_ind} __ fitness: {round(best.fitness,4)}")

    logging.info("--- %s seconds ---" % (round((time.time() - start_time),3)))

if __name__ == '__main__':
    try:
        gpc = GpControl()
        gpc.undertake_run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
