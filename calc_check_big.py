import numpy as np
import sys
import teneva


from opts import Opts
from plot import plot_check_big
from utils import Log


def plot_appr_check_big(opts, names):
    data = {}
    for name in names:
        fpath = opts.fold + f'/res/res_appr_check_big_{name}.npz'
        data[name] = np.load(fpath, allow_pickle=True).get('res').item()
        r_list = list(data[name].keys())
        s_list = list(data[name][r_list[0]].keys())

    fpath = opts.fold + f'/plot/check_big.png'
    plot_check_big(data, r_list, s_list, fpath)


def run_appr_check_big(opts, name):
    name = name or opts.name_check

    log = Log(f'{opts.fold}/logs/appr_check_big_{name}.txt')
    opts.prep_funcs()
    opts.prep_pde(with_prep=False)

    log(opts.info(is_check=True, name=name))

    func = opts.get_func(name)
    func.load_trn_ind(opts.get_fpath(func, 'trn_ind'))
    func.load_tst_ind(opts.get_fpath(func, 'tst_ind'))

    res = {}
    for r in [4, 6, 8]:
        res[r] = {}

        func.anova(r=r, order=opts.order, noise=opts.noise_ano)
        Y = teneva.copy(func.Y)

        for nswp in opts.nswp_check_big:
            t_als_rnd = []
            e_als_rnd = []

            func.clear()
            func.prep(Y)
            func.als(nswp=nswp, e=None)
            t_als_ano = func.t
            e_als_ano = func.check_tst_ind()

            res[r][nswp] = {
                't_als_ano': t_als_ano,
                'e_als_ano': e_als_ano,
            }

            text = f'r: {r:-1d} | nswp: {nswp:-4d} | '
            text += f'e_als_ano = {e_als_ano:-7.1e} | t = {t_als_ano:-7.3f}'
            log(text)
        log('')

        fpath = opts.fold + f'/res/res_appr_check_big_{name}.npz'
        np.savez_compressed(fpath, res=res)


if __name__ == '__main__':
    np.random.seed(42)

    run_appr_check_big(Opts(), 'Dixon')
    run_appr_check_big(Opts(), 'Piston')
    run_appr_check_big(Opts(), 'PDE-VOI')

    plot_appr_check_big(Opts(), ['Dixon', 'Piston', 'PDE-VOI'])
