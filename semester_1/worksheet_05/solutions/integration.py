#!/usr/bin/env python
import argparse
import numpy as np
from sympy import *
from sympy.utilities.lambdify import implemented_function, lambdify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from sampling import simple_sampling

parser = argparse.ArgumentParser()
parser.add_argument('--simple', help="Exercise 2", action="store_true")
parser.add_argument('--test', help="Testing mode", action="store_true")
args = parser.parse_args()


#def f(x):
 #   return (-2*x*x * np.sin(x) * np.cos(x) - 2*x* np.sin(x)*np.sin(x)) * np.exp(-x*x * np.sin(x) * np.sin(x))


def plot_simple():
    init_printing(use_unicode=False, wrap_line=False)
    x = Symbol('x')
    expression = (-2*x*x * sin(x) * cos(x) - 2*x* sin(x)*sin(x)) * exp(-x*x * sin(x) * sin(x))

    with PdfPages("plots/simple.pdf") as pdf:
        x_range = np.linspace(0.1, 50, 1000)
        f = lambdify(x, expression)

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.plot(x_range, f(x_range), label='Computed Function', linewidth=0.7, color='tab:blue')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()

        x_range = range(2, 21)
        actual = N(integrate(expression, (x, 0.1, 50)))
        approx, approx_err = np.array([simple_sampling(f, 0.1, 50, 1<<i) for i in x_range]).T

        plt.xlabel(r"$\log_2 N$")
        plt.ylabel("Integration Value")
        plt.plot(x_range, len(x_range)*[actual], label="Exact solution", linewidth=0.7, color='tab:blue')
        plt.errorbar(x_range, approx, approx_err, None, '.', capsize= 1.4, linewidth=0.7, label="Monte Carlo approximation", color='tab:red')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()

        plt.xlabel(r"$\log_2 N$")
        plt.ylabel("Error Value")
        plt.plot(x_range, np.abs(approx-actual), ".", label="Actual error", linewidth=0.7, color='tab:blue')
        plt.plot(x_range, approx_err, ".", label="Statistical error", linewidth=0.7, color='tab:red')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    if args.simple:
        plot_simple()

    if args.test:
        for _ in range(10):
            print(simple_sampling(lambda x: x, 0, 1, 1_000_000))
            