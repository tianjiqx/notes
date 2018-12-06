
#include<iostream>
#include<map>
#include<algorithm>

using namespace std;

//key value >0

typedef struct node {
    int key;
    int value;
    node * next;
    node * head;
    node(int k, int v) {
        key = k;
        value = v;
        next = NULL;
        head = NULL;
    }

} node;


class Qlist {

public:

    node * head;

public:
    Qlist() {
        head = new node(-1, -1);
        head->head = head;
        head->next = head;
    }


    //insert
    void insert(node * n) {
        if (n == NULL) {
            return;
        }

        n->next = head->next;
        head->next->head = n;
        n->head = head;
        head->next = n;
    }

    //delete
    int del(node * n) {
        if (n == NULL) {
            return -1;
        }

        n->head->next = n->next;
        n->next->head = n->head;
        int ret = n->key;
        delete n;
        return ret;
    }

    //delete back
    int pop_back() {
        if (head->head != head) {
            return del(head->head);
        } else {
            return -1;
        }
    }

    //move front
    node*  movefront(node * n) {
        if (n == NULL) {
            return NULL;
        } else if(n == head->next) { //not need move
            return n;
        } else { //move
            //lazy reuse node Orz.
            node *tmp = new node(n->key, n->value);
            //first delete,then insert into front
            del(n);
            insert(tmp);
            return tmp;
        }
    }
    void traverse() {
        node *tmp = head->next;
        cout << "traverse:";
        while(tmp != head) {
            cout << " key=" << tmp->key << " value=" << tmp->value;
            tmp = tmp->next;
        }
        cout << endl;
    }

};


typedef map<int, node *> M1;

class LRUCache {

public:
    int cap;
    M1 m;
    Qlist l;
    int count;
public:
    LRUCache(int capacity) {
        cap = capacity;
        count = 0;
    }

    int get(int key) {
        M1::iterator it = m.find(key);
        if (it != m.end()) {
            int ret = (*it).second->value;
            //cout<<"GET:"<<(*it).first<<" "<<(*it).second<<endl;
            node *newpos = l.movefront((*it).second);
            (*it).second = newpos;
            return ret;
        } else {
            return -1;
        }
    }

    void put(int key, int value) {

        if (m.find(key) != m.end()) {
            return;
        }


        node *n = new node(key, value);
        m.insert(M1::value_type(key, n));
        if(count < cap) {
            l.insert(n);
            count++;
        } else {

            int delkey = l.pop_back();
            l.insert(n);
            //del elimite key from map
            m.erase(m.find(delkey));
        }
    }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */

int main() {

    LRUCache lru(2);

    lru.put(1, 2);
    lru.put(2, 3);
    lru.l.traverse();
    cout << "get key=1 :" << lru.get(1) << endl;
    lru.l.traverse();
    cout << "get key=2 :" << lru.get(2) << endl;
    lru.l.traverse();
    cout << "get key=1 :" << lru.get(1) << endl;
    lru.l.traverse();
    lru.put(3, 4);
    lru.l.traverse();
    cout << "get key=2 :" << lru.get(2) << endl;
    lru.l.traverse();
    cout << "get key=3 :" << lru.get(3) << endl;
    lru.l.traverse();

    return 0;
}

