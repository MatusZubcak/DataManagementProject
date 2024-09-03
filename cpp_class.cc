#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cmath>
#include <bits/stdc++.h>

using namespace std;

struct Find_optimal_universum_size {
    Find_optimal_universum_size() {}

    int compute(int m, int n) {
        int best_k = -1;
        double best = -INFINITY;
        for (int k = m; k < 2500; ++k) {

            double log_comb = 0;
            for (int i = 0; i < m; ++i) {
                log_comb += log(k - i) - log(std::max(i, 1));
            }
            double curr = log_comb - n * log(k);


            if (best < curr) {
            best_k = k;
            best = curr;
            }
        }
        return best_k;
}
};

PYBIND11_MODULE(cpp_function, m) {
    pybind11::class_<Find_optimal_universum_size>(m, "Find_optimal_universum_size")
        .def(pybind11::init())
        .def("compute", &Find_optimal_universum_size::compute);
}
