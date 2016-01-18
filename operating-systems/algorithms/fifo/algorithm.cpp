#include <iostream>
#include <string>
#include <sstream>

using namespace std;

class Node {
	public:
		string page;
		Node* next;
};

class Queue {
	private:
		Node* first;
		Node* last; 
		int N;

	public:
		int size() {
			return N;
		}

		bool isEmpty() {
			return N == 0;
		}

		Node* peek() {
			return first;
		}

		void enqueue(string page) {
			Node* oldlast = last;
			last = new Node(); 
			last->page = page;
			if (isEmpty()) first = last; 
			else oldlast->next = last; 
			N++;
		}
		
		string dequeue() {
			string page = first->page; 
			first = first->next;
			if (isEmpty()) last = NULL;
			N--;
			return page;
		}

};