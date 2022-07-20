import os


class Log:
    def __init__(self, fpath='log.txt'):
        self.fpath = fpath
        self.is_new = True
        self.len_pref = 19

    def __call__(self, text):
        print(text)
        with open(self.fpath, 'w' if self.is_new else 'a') as f:
            f.write(text + '\n')
        self.is_new = False

    def name(self, name):
        text = name + ' ' * max(0, self.len_pref-len(name)) + ' > '
        self(text)

    def res(self, res):
        name = res['method']
        text = '  - ' + name + ' ' * max(0, self.len_pref-len(name)-4) + ' | '

        text += 'error (trn/tst) : '
        text += f'{res["e_trn"]:-7.1e} / '
        text += f'{res["e_tst"]:-7.1e}'

        if 't' in res:
            text += ' | time : '
            text += f'{res["t"]:-7.3f}'

        self(text)

    def res_data(self, t, m, name):
        text = '  - ' + name + ' ' * max(0, self.len_pref-len(name)-4) + ' | '
        text += 'samples : '
        text += f'{m:-7.1e} | '
        text += 'time : '
        text += f'{t:-8.4f}'
        self(text)


def folder_ensure(fpath):
    if not os.path.exists(fpath):
        os.makedirs(fpath)
