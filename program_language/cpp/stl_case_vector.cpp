#include<iostream>
#include<vector>
#include<algorithm>

#include<string>

using namespace std;



//desc cmp function
bool cmp(const int a, const int b) {

    return a > b;

}


int main() {

    //create
    vector<int> v1;
    vector<int> v2(v1); // <=> vector<int> v2=v1
    vector<int> v3(10, 1); // init 1,1,1,1,1,1...
    //vector<T> v4(10);  call T type constructor function
    //vector<int> v5={ 1,2,3,4 };// <=> vector<int> v5{1,2,3,4}
    vector<vector<int> > v6;  // v6[][]
    vector<string> v7(3, "abc");

    int arr[] = {1, 2, 3, 4};
    vector<int> v5(arr, arr + 4);


    //inset
    v7.push_back("def");
    v7.push_back("fgg");
    v7.insert(v7.begin() + 2, "xxx"); //insert in secode pos
    cout << "v7[2]:" << v7[2] << endl;
    //size()
    cout << "v7 element number :" << v7.size() << endl;
    cout << "v5 element number :" << v5.size() << endl;


    //travese
    cout << "v7:\n";
    for (int i = 0; i < v7.size(); i++) {
        cout << v7[i] << endl;
    }

    cout << "v5:\n";
    vector<int>::iterator it = v5.begin();
    for (; it != v5.end(); it++) {

        cout << *it << endl;
    }

    //pop_back()  delete tailf element
    //erase
    v5.erase(v5.begin() + 1); //delelete 2th element

    cout << "erase v5.beign()+1:\n";
    it = v5.begin();
    for (; it != v5.end(); it++) {

        cout << *it << endl;
    }
    //erase 2 elements
    v7.erase(v7.begin() + 1, v7.begin() + 3);
    cout << "erase v7.beign()+1,+3:\n";

    for (int i = 0; i < v7.size(); i++) {
        cout << v7[i] << endl;
    }


    v5.push_back(2);
    v5.push_back(1);
    v5.push_back(7);
    v5.push_back(3);

    //sort
    sort(v5.begin(), v5.end());
    cout << "sort v5:\n";
    it = v5.begin();
    for (; it != v5.end(); it++) {

        cout << *it << endl;
    }

    //sort
    sort(v5.begin(), v5.end(), cmp);
    cout << "sort v5 cmp:\n";
    it = v5.begin();
    for (; it != v5.end(); it++) {

        cout << *it << endl;
    }




    return 0;
}




