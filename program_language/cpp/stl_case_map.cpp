#include<iostream>
#include<map>
#include<string>

using namespace std;


int main() {



    //create
    typedef map<string, int> M;
    M m1;

    string str = "abc";
    int value = 1;

    //insert
    m1.insert(M::value_type(str, value));
    m1.insert(M::value_type("cde", 2));


    //traverse
    M::iterator it = m1.begin();
    while(it != m1.end()) {

        cout << it->first << "  " << it->second << endl;
        it++;
    }


    //size
    cout << "map m1 element number :" << m1.size() << endl;


    //find and count element
    if (m1.find(str) == m1.end()) {

        cout << "key " << str << " is not exists!\n";
    } else {

        cout << "key " << str << " is exists!\n"; //output

    }


    if (m1.count(str) == 0) {

        cout << "key " << str << " is not exists!\n";
    } else {

        cout << "key " << str << " is exists!\n"; //output
    }


    if (m1.find("edf") == m1.end()) {

        cout << "key " << "edf" << " is not exists!\n"; //output
    } else {

        cout << "key " << "edf" << "is exists!\n";
    }

    //update
    m1["abc"] = 2;
    cout << "abc " << m1["abc"] << endl;

    m1.at("abc") = 3;
    cout << "abc " << m1.at("abc") << endl;



    //erase by key
    m1.erase("abc");
    // erase by it
    m1.erase(m1.find("cde"));
    //erase range bein - 'cde'
    // m1.erase(m1.begin(),m1.find("cde")++);


    cout << "after erase:\n";
    it = m1.begin();
    while(it != m1.end()) {

        cout << it->first << "  " << it->second << endl;
        it++;
    }

    //clear
    m1.clear();

    return 0;
}




