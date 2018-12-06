#include<iostream>
#include<string>

#include<map>
#include<vector>


using namespace std;


/*
 * c++ input an output case
 *
 *
 *
 *
 */


int main() {

    int len = 0;
    string str;

    typedef map<string, int> M;
    M m1;

    // input string
    // eg:
    // aaa ddd
    // ccc eee
    // ccc ddd
    while (cin >> str) {

        if (m1.find() != m1.end()) {
        } else {
            //insert one
            m1.insert(M::value_type(str, 1));
            len++;

        }
    }
    // output distinct value number
    cout << len;

}

