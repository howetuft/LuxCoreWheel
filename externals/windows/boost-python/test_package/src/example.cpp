#include "boost-python.h"
#include <vector>
#include <string>

int main() {
    boost_python();

    std::vector<std::string> vec;
    vec.push_back("test_package");

    boost_python_print_vector(vec);
}
