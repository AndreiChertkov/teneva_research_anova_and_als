import numpy as np
import sys


from opts import Opts
from utils import Log


def calc_als(func, opts, log):
    func.clear()
    func.rand(r=opts.r)
    func.als(nswp=opts.nswp, log=opts.with_log)

    t = func.t
    e_trn = func.check_trn_ind()
    e_tst = func.check_tst_ind()
    log.res({'method': func.method, 't': t, 'e_trn': e_trn, 'e_tst': e_tst})

    return t, e_trn, e_tst


def calc_als_many(func, opts, log):
    t = []
    e_trn = []
    e_tst = []
    for rep in range(opts.reps):
        t_cur, e_trn_cur, e_tst_cur = calc_als(func, opts, log)
        t.append(t_cur)
        e_trn.append(e_trn_cur)
        e_tst.append(e_tst_cur)

    t = np.mean(t)
    e_trn = np.mean(e_trn)
    e_tst = np.mean(e_tst)
    if opts.reps > 1:
        method = 'ALS (* mean)'
        log.res({'method': method, 't': t, 'e_trn': e_trn, 'e_tst': e_tst})

    return t, e_trn, e_tst


def calc_ano(func, opts, log):
    func.clear()
    func.anova(r=opts.r, order=opts.order, noise=opts.noise_ano)

    t = func.t
    e_trn = func.check_trn_ind()
    e_tst = func.check_tst_ind()
    log.res({'method': func.method, 't': t, 'e_trn': e_trn, 'e_tst': e_tst})

    return t, e_trn, e_tst


def calc_ano_als(func, opts, log):
    func.clear()
    func.anova(r=opts.r, order=opts.order, noise=opts.noise_ano)
    func.als(nswp=opts.nswp, log=opts.with_log)

    t = func.t
    e_trn = func.check_trn_ind()
    e_tst = func.check_tst_ind()
    log.res({'method': func.method, 't': t,
        'e_trn': e_trn, 'e_tst': e_tst})

    return t, e_trn, e_tst


def run_appr(opts, with_noise=False):
    """Run computations with approximation of benchmark functions and PDE."""
    if with_noise:
        # (note: we do not apply noise to PDE, only for benchmarks)
        log = Log(f'{opts.fold}/logs/appr_noise.txt')
        opts.prep_funcs()
    else:
        log = Log(f'{opts.fold}/logs/appr.txt')
        opts.prep_funcs()
        opts.prep_pde(with_prep=False)

    text =  '\n\n' + '='*70 + '\nLatex code for table : \n\n'
    log(opts.info())

    for func in opts.funcs_appr:
        log.name(func.name)

        if with_noise:
            func.set_noise(noise_mul=opts.noise)

        func.load_trn_ind(opts.get_fpath(func, 'trn_ind'))
        func.load_tst_ind(opts.get_fpath(func, 'tst_ind'))

        t_als, e_als_trn, e_als_tst = calc_als_many(func, opts, log)
        t_ano, e_ano_trn, e_ano_tst = calc_ano(func, opts, log)
        t_ano_als, e_ano_als_trn, e_ano_als_tst = calc_ano_als(func, opts, log)

        text += '\n\\multirow{2}{*}{' + func.name + '}'
        text += '\n& Train & '
        text += f'{e_ano_trn:-7.1e} & '
        text += f'{e_als_trn:-7.1e} & '
        text += f'{e_ano_als_trn:-7.1e} '
        text += '\\\\ '
        text += '\n& Test  & '
        text += f'{e_ano_tst:-7.1e} & '
        text += f'{e_als_tst:-7.1e} & '
        text += f'{e_ano_als_tst:-7.1e} '
        text += '\\\\ '
        text += '\\hline'

    log(text)


def run_data(opts, with_funcs=True, with_pde=False):
    """Prepare train and test data for benchmark functions and PDE."""
    if with_funcs:
        log = Log(f'{opts.fold}/logs/data.txt')
        opts.prep_funcs()
    if with_pde:
        log = Log(f'{opts.fold}/logs/data_pde.txt')
        opts.prep_pde()

    for func in opts.funcs_appr:
        log.name(func.name)

        func.build_trn_ind(opts.m_trn)
        func.save_trn_ind(opts.get_fpath(func, 'trn_ind'))
        log.res_data(func.t_trn_ind_build, func.m_trn_ind, 'trn_ind')

        func.build_tst_ind(opts.m_tst)
        func.save_tst_ind(opts.get_fpath(func, 'tst_ind'))
        log.res_data(func.t_tst_ind_build, func.m_tst_ind, 'tst_ind')


if __name__ == '__main__':
    np.random.seed(42)

    mode = sys.argv[1] if len(sys.argv) > 1 else 'appr'
    device = sys.argv[2] if len(sys.argv) > 2 else 'pc'
    fold = sys.argv[3] if len(sys.argv) > 3 else 'result'

    gmsh_path = 'gmsh/build/gmsh' if device == 'docker' else None

    opts = Opts(fold, gmsh_path)

    if mode == 'appr':
        run_appr(opts)
    elif mode == 'appr_noise':
        run_appr(opts, with_noise=True)
    elif mode == 'data':
        run_data(opts, with_funcs=True, with_pde=False)
    elif mode == 'data_pde':
        run_data(opts, with_funcs=False, with_pde=True)
    else:
        raise ValueError(f'Invalid computation mode "{mode}"')
