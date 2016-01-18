#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Widget.H>
#include <FL/Fl_Box.H>
#include <FL/Fl_Input.H>
#include <FL/Fl_Int_Input.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Menu_Bar.H>
#include <FL/Fl_JPEG_Image.H>

#include <iostream>
#include <string>
#include <sstream>

#include "algorithm.cpp"

using namespace std;

int size = 10;
int pagesCount = 0;
Queue *queue;
Fl_Box **pages;
Fl_Box *pageAddInfo;
Fl_Box *pageDelInfo;
Fl_Window *startWindow;
Fl_Window *mainWindow; 
Fl_Window *aboutWindow;

void on_press_add_new_page(Fl_Widget *, void *w) {

	Fl_Input *pageInput = (Fl_Input*) w;

	stringstream temp;
	temp << pageInput->value();
	string pageName = temp.str();

	if (pageName == "") return;

	Node *current = queue->peek();
	while (current != NULL) {
		if (pageName == current->page) return;
		current = current->next;
	}

	if (pagesCount == size) pagesCount = 0;

	queue->enqueue(pageName);

	char *charArrayResult = new char[pageName.size()+1];
	charArrayResult[pageName.size()] = 0;
	memcpy(charArrayResult, pageName.c_str(), pageName.size());

	pageAddInfo->label(charArrayResult);
	
	pageName = queue->dequeue();

	charArrayResult = new char[pageName.size()+1];
	charArrayResult[pageName.size()] = 0;
	memcpy(charArrayResult, pageName.c_str(), pageName.size());

	pageDelInfo->label(charArrayResult);
	
	string result = "";

	current = queue->peek();
	while (current != NULL) {
		result += current->page; 
		result += "  ";
		current = current->next;
	}
	charArrayResult = new char[result.size()+1];
	charArrayResult[result.size()] = 0;
	memcpy(charArrayResult, result.c_str(), result.size());

	pages[pagesCount++]->label(charArrayResult);
}

void on_press_continue_btn(Fl_Widget *, void *w) {
	Fl_Int_Input *input = (Fl_Int_Input*) w; 
	int workplace = atoi(input->value()); 
	if (workplace > 10) workplace = 5;
	
	queue = new Queue();
	int amount = workplace;
	
	stringstream temp;
	temp << -1;
	string pageName = temp.str();
	while (amount-- != 0)
		queue->enqueue(pageName);
	
	for (int i = 0; i < size; i++)
		pages[i]->label("");
	pageAddInfo->label("-1");
	pageDelInfo->label("-1");

	pagesCount = 0;
	mainWindow->show(); 
	startWindow->hide();
}

void on_press_quit_menu(Fl_Widget *, void *) {
	exit(0);
}

void on_press_about_menu(Fl_Widget *, void *) {
	aboutWindow->show();
}

void on_press_new_menu(Fl_Widget *, void *w) {
	mainWindow->hide();
	aboutWindow->hide();
	startWindow->show();
}

int main() {
	startWindow = new Fl_Window(400, 200, "New");
	startWindow->begin();
	Fl_Int_Input pagesIntInput(200, 50, 100, 30, "Workplace : ");
	pagesIntInput.labelfont(FL_BOLD);
	pagesIntInput.value("5");
	Fl_Button continueBtn(150, 125, 100, 30, "Continue");
	continueBtn.color(FL_YELLOW);
	continueBtn.callback(on_press_continue_btn, &pagesIntInput);
	startWindow->end();
	startWindow->show();


	aboutWindow = new Fl_Window(400, 200, "About");
	aboutWindow->begin();
	Fl_Box aboutBox(0, 0, 400, 200, "FIFO cache\n\302\251 Ekaterina Melyanets 2016");
	aboutWindow->end();


	mainWindow = new Fl_Window(700, 600, "FIFO cache");
	mainWindow->begin();

	Fl_Box imageBox(0, 0, 700, 700);
	Fl_JPEG_Image jpg("image.jpg");
	imageBox.image(jpg);

	Fl_Menu_Bar menuBar(0, 0, 700, 25);
	menuBar.add("File/New", FL_CTRL+'n', on_press_new_menu);
	menuBar.add("File/Quit", FL_CTRL + 'q', on_press_quit_menu);
	menuBar.add("Help/About", FL_CTRL + 'a', on_press_about_menu);

	Fl_Box pageAddLabel(460, 180, 50, 30, "Added :");
	Fl_Box pageDelLabel(460, 210, 50, 30, "Deleted :");
	pageAddInfo = new Fl_Box(550, 180, 50, 30, "-1");
	pageAddInfo->labelfont(FL_COURIER_BOLD);
	pageDelInfo = new Fl_Box(550, 210, 50, 30, "-1");
	pageDelInfo->labelfont(FL_COURIER_BOLD);

	pages = new Fl_Box*[size];
	int y = 50; 
	for (int i = 0; i < size; i++) {
		*(pages + i) = new Fl_Box(50, y, 300, 40, "");
		pages[i]->box(FL_SHADOW_BOX);
		pages[i]->labelfont(FL_COURIER_BOLD_ITALIC);
		y += 50;
	}

	Fl_Input pageInput(450, 70, 150, 30, "Enter new page");
	pageInput.align(FL_ALIGN_TOP);

	Fl_Button addPageBtn(450, 105, 150, 30, "Add");
	addPageBtn.color(FL_WHITE);

	addPageBtn.callback(on_press_add_new_page, &pageInput);
	mainWindow->end();

	return Fl::run();
}