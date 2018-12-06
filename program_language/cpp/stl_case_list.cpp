#include<iostream>
#include<list>
#include <algorithm>
#include <iterator>
using namespace std;

int main() {


    int arr[] = {1, 2, 3, 4, 5};
    list<int> l1;

    //assign form arrary
    l1.assign(arr, arr + 5);



    //create
    list<int> l2(5); // create 5 default element
    list<int> l3(5, 1); // l3: 1 1 1 1 1


    list<int>::iterator it = l1.begin();
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }

    cout << "\n";

    it = find(l1.begin(), l1.end(), 2);

    cout << "pos 2= " << *it << endl;

    cout << "l1 front()=" << l1.front() << " l1 back()" << l1.back() << endl;

    //erase
    l1.erase(l1.begin(), it);

    it = l1.begin();

    cout << "after erase\n";
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }

    //insert
    it = l1.insert(l1.begin(), 10);
    cout << "insert " << *it << endl;
    it = l1.begin();
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }

    //sort
    l1.sort();
    cout << "sort:\n";
    it = l1.begin();
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }


    //merge asc order free l3
    l1.merge(l3);
    cout << "merge:\n";
    it = l1.begin();
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }

    cout << "l3 size=" << l3.size() << endl;


    //push back
    l1.push_back(13);
    cout << "push back 13\n";
    it = l1.begin();
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }
    cout << "l1 size:" << l1.size() << endl;
    //remove  all =1
    l1.remove(1);
    cout << "remove:\n";
    it = l1.begin();
    for(; it != l1.end(); it++) {
        cout << *it << " ";
    }
    cout << "l1 size=" << l1.size() << "\n";



    return 0;

}


