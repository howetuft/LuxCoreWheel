#include "foo.h"
#include <vector>
#include <string>

int main() {
    foo();

    std::vector<std::string> vec;
    vec.push_back("test_package");

    foo_print_vector(vec);
}
