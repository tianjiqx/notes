#include<iostream>
#include<string>
#include<algorithm>
using namespace std;


int main() {



    string s1 = "abcd";

    string s2(s1);

    string s3(10, 'a'); // aaaaa.... a  (10)

    string s4;
    cin >> s4; //wait space , aa aaa => s4="aa"
    string s5;
    getline(cin, s5); //wait enter, aa aaa \n  -> s5='aa aaa'
    string s6;
    getline(cin, s6, 'a'); //end with 'a', dffgh f \n ff ba -> s6='dffgh f \n ff b'

    //size
    cout << s1.size() << " " << s1.length() << endl;


    //read
    cout << s1[0];
    //concate
    s4 = s1 + s2;
    //compare
    if (s1 == s2) {
        cout << "s1==s2\n";
    } else {
        cout << "s1!=s2\n";
    }


    //insert
    s2.insert(s2.begin(), 'b');

    //substr
    int strlen = 4;
    s1 = s1.substr(1, strlen); // retrun s1[1:1+strlen]
    s2 = s2.substr(1) ; // retrun s2[1:]

    //find
    s1.find("abc");  // return first index,or -1
    //compare
    s1.compare("abc"); // =  0, > 1, < -1
    //reverse
    reverse(s1.begin(), s1.end()); //

    return 0;
}



