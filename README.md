# teneva_research_anova_and_als


## Description

Numerical experiments for **TT-ANOVA** and **TT-ALS** methods from [teneva](https://github.com/AndreiChertkov/teneva) python package. These methods are designed to approximate nultidimensional arrays (tensors) and multivariable functions (black boxes) by low-rank tensor train (TT) decomposition. As numerical examples, we consider benchmark (analytic) functions and parametric partial differential equation.


## Basic usage

1. Install [python](https://www.python.org) programming language interpreter (the version >= 3.7) as a part of [anaconda](https://www.anaconda.com)

2. Create virtual environment with `fenics`:
    ```bash
    conda create -n teneva_research_anova_and_als -c conda-forge fenics
    ```

3. Activate the created virtual environment:
    ```bash
    conda activate teneva_research_anova_and_als
    ```

4. Install all required dependencies:
    ```bash
    pip install numpy gmsh teneva==0.9.16
    ```

5. Run the script:
    ```bash
    python calc.py FLAG
    ```
    with the flag:
    - `data` - generate and save train/test data for benchmark functions
    - `data_pde` - generate and save train/test data for parametric PDE
    - `appr` - build approximation from the saved data for benchmark functions and parametric PDE
    - `appr_noise` (build approximation from the saved data with automatically added noise).

    > The results and logs will be saved into `result` folder

    > Note that computation options are set in `opts.py` script.

    > You can also optionally run the script `python pde/demo_solve.py` with demonstration of the PDE solver work

6. At the end of the work, you can, if necessary, delete the environment:
    ```bash
    conda activate && conda remove --name teneva_research_anova_and_als --all
    ```


## Usage with docker

1. Configure and run docker with `fenics`:
    1. ... (use curl command from site `https://fenicsproject.org/download/`)
    2. Run `docker` as `sg docker bash` and then, e.g., `/home/andrei_chertkov/.local/bin/fenicsproject run`
    3. To exit `docker`, run `exit`
2. Prepare repository:
    1. `git clone https://github.com/AndreiChertkov/teneva_research_anova_and_als.git`
    2. `cd teneva_research_anova_and_als`
    3. Optionally create a working environment:
        1. `conda create -n teneva_research_anova_and_als -c conda-forge fenics`
        2. `conda activate teneva_research_anova_and_als`
    4. Update packages `pip install --upgrade pip numpy scipy teneva==0.9.16 --user`;
3. Install `gmsh` (from the root of the project):
    1. `git clone https://gitlab.onelab.info/gmsh/gmsh.git`
    2. `cd gmsh && mkdir build && cd build`
    3. `cmake ..`
    4. `make`
    5. `cd ./../../`
4. Run the script `python3 calc.py FLAG docker` (possible flag values have been described above; the 2th argument must be specified only if the calculation is performed from `docker`).


## Authors

- [Andrei Chertkov](https://github.com/AndreiChertkov)
- [Gleb Ryzhakov](https://github.com/G-Ryzhakov)
- [Ivan Oseledets](https://github.com/oseledets)
