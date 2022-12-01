import numpy as np
import sys


from opts import Opts
from plot import plot_check
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


def run_appr_check(opts, name=None):
    """Check dependence of the approximation accuracy vs rank, etc."""
    name = name or opts.name_check

    log = Log(f'{opts.fold}/logs/appr_check_{name}.txt')
    opts.prep_funcs()
    opts.prep_pde(with_prep=False)

    log(opts.info(is_check=True, name=name))

    func = opts.get_func(name)
    func.load_trn_ind(opts.get_fpath(func, 'trn_ind'))
    func.load_tst_ind(opts.get_fpath(func, 'tst_ind'))

    res = {}
    for r in opts.r_check:
        res[r] = {}
        for nswp in opts.nswp_check:
            t_als_rnd = []
            e_als_rnd = []
            for rep in range(opts.reps):
                func.clear()
                func.rand(r=r)
                func.als(nswp=nswp)
                t_als_rnd.append(func.t)
                e_als_rnd.append(func.check_tst_ind())

            func.clear()
            func.anova(r=r, order=opts.order, noise=opts.noise_ano)
            func.als(nswp=nswp)
            t_als_ano = func.t
            e_als_ano = func.check_tst_ind()

            res[r][nswp] = {
                't_als_rnd': np.mean(t_als_rnd),
                't_als_ano': t_als_ano,
                'e_als_rnd': e_als_rnd,
                'e_als_ano': e_als_ano,

            }

            text = f'r: {r:-1d} | nswp: {nswp:-3d} | '
            text += f'e_als_rnd = {np.mean(e_als_rnd):-7.1e} | '
            text += f'e_als_ano = {e_als_ano:-7.1e} | '
            log(text)

        fpath = opts.fold + f'/res/res_appr_check_{name}.npz'
        np.savez_compressed(fpath, res=res)


def run_appr_check_all(opts):
    """Check approximation accuracy for all functions."""
    for name in opts.names_check:
        print(f'\n\n\n>>> Function "{name}" >>>')
        run_appr_check(opts, name)


def run_appr_check_show(opts, name=None, r_draw=5, s_draw=100):
    """Demonstrate the result of the "run_appr_check" function."""
    name = name or opts.name_check

    fpath = opts.fold + f'/res/res_appr_check_{name}.npz'
    res = np.load(fpath, allow_pickle=True).get('res').item()
    r_list = list(res.keys())
    s_list = list(res[r_list[0]].keys())

    print('Function : ', name)
    print('Ranks    : ', r_list)
    print('Sweeps   : ', s_list)
    print('Results  : ')

    for r in r_list:
        for s in s_list:
            e_als_rnd = res[r][s]['e_als_rnd']
            e_als_ano = res[r][s]['e_als_ano']

            text = f'>>>>>>>>>> rank : {r:-3d} | nswp : {s:-3d} | '
            text += f'e_als_rnd : {np.mean(e_als_rnd):-7.1e} | '
            text += f'e_als_rnd_var : {np.var(e_als_rnd):-7.1e} | '
            text += f'e_als_ano : {e_als_ano:-7.1e} | '
            print(text)

    r_list = [2, 4, 6, 8, 10]
    plot_check(res, name, r_list, fpath=opts.fold + f'/plot/{name}.png')


def run_appr_check_show_all(opts):
    """Demonstrate the result of the "run_appr_check_all" function."""
    for name in opts.names_check:
        print(f'\n\n\n>>> Function "{name}" >>>')
        run_appr_check_show(opts, name)


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
    elif mode == 'appr_check':
        run_appr_check(opts)
    elif mode == 'appr_check_all':
        run_appr_check_all(opts)
    elif mode == 'appr_check_show':
        run_appr_check_show(opts)
    elif mode == 'appr_check_show_all':
        run_appr_check_show_all(opts)
    elif mode == 'appr_noise':
        run_appr(opts, with_noise=True)
    elif mode == 'data':
        run_data(opts, with_funcs=True, with_pde=False)
    elif mode == 'data_pde':
        run_data(opts, with_funcs=False, with_pde=True)
    else:
        raise ValueError(f'Invalid computation mode "{mode}"')
