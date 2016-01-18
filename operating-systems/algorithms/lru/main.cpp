#include <FL/Fl.H>
#include <FL/Fl_Int_Input.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Box.H>
#include <FL/Fl_Widget.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Menu_Bar.H>
#include <FL/Fl_Tabs.H>
#include <FL/Fl_Group.H>
#include <FL/Fl_Text_Buffer.H>
#include <FL/Fl_Text_Display.H>
#include <FL/Fl_JPEG_Image.H>

#include <iostream>
#include <sstream>
#include <stdint.h>

#include "algorithm.cpp"

using namespace std;

int inputSize = 16;
int count = 0;
Fl_Box **workplaceBox;
Fl_Box **nowpageBox;

Fl_Window *aboutWindow;
Fl_Window *contentsWindow;

Cache *cache = new Cache();

void on_press_read_btn(Fl_Widget*, void *w) {
	if (count == inputSize) return;
	Fl_Int_Input *pageInput = (Fl_Int_Input*)w;
	int pageName = atoi(pageInput->value());

	cache->push(pageName);
	Page *workplace = cache->workplace;

	string result;
	stringstream ss;
	ss << pageName;
	result = ss.str();
	char *charArrayResult = new char[result.size()+1];
	charArrayResult[result.size()] = 0;
	memcpy(charArrayResult, result.c_str(), result.size());

	nowpageBox[count]->label(charArrayResult);

	result = "";
	for (int i = 0; i<cache->workplaceSize; i++) {
		stringstream ss;
		ss<<workplace[i].name;
		result += ss.str() += "  ";
	}
	charArrayResult = new char[result.size()+1];
	charArrayResult[result.size()] = 0;
	memcpy(charArrayResult, result.c_str(), result.size());

	workplaceBox[count++]->label(charArrayResult);
}

void on_press_quit_menu(Fl_Widget *, void *) {
	exit(0);
}

void on_press_about_menu(Fl_Widget *, void *) {
	aboutWindow->show();
}

void on_press_contents_menu(Fl_Widget *, void *) {
	contentsWindow->show();
}

void on_press_new_menu(Fl_Widget *, void *) {
	cache = new Cache();
	count = 1;
	for (int i = 1; i < inputSize; i++) {
		workplaceBox[i]->label("");
		nowpageBox[i]->label("");
	}
}

int main(int argc, char *argv[]) {

	aboutWindow = new Fl_Window(500, 200, "About");
	aboutWindow->begin();
	Fl_Box aboutBox(0, 0, 500, 200, "LRU cache\n\302\251 2016 Elena Kasatkina");
	aboutWindow->end();

	contentsWindow = new Fl_Window(500, 500, "Help");
	contentsWindow->begin();
	Fl_Tabs tabs(10, 10, 480, 480);
	Fl_Group content1(10, 35, 470, 445, "What is lru?");
	Fl_Text_Buffer *buff = new Fl_Text_Buffer();
	Fl_Text_Display display(11, 36, 479, 454, "");
	Fl_Color GREEN();
	display.buffer(buff);
	buff->loadfile("help1.txt");
	content1.end();
	
	Fl_Group content2(10, 35, 480, 455, "Algorithm");
	Fl_Text_Buffer *buff2 = new Fl_Text_Buffer();
	Fl_Text_Display display2(11, 36, 479, 454, "");
	display2.buffer(buff2);
	buff2->loadfile("help2.txt");
	content2.end();

	contentsWindow->end();


	Fl_Window mainWindow(700, 700, "LRU cache");
	mainWindow.begin();

	Fl_Box imageBox(0, 0, 700, 700);
	Fl_JPEG_Image jpg("image.jpg");
	imageBox.image(jpg);
	
	Fl_Menu_Bar menuBar(0, 0, 700, 25);
	menuBar.add("File/New", FL_CTRL + 'n', on_press_new_menu);
	menuBar.add("File/Quit", FL_CTRL + 'q', on_press_quit_menu);
	menuBar.add("Help/About", FL_CTRL + 'a', on_press_about_menu);
	menuBar.add("Help/Contents", FL_F + 1, on_press_contents_menu);
	Fl_Int_Input pageInput(150, 50, 100, 30, "Enter the page:");
	pageInput.labelsize(16);
	Fl_Button readBtn(250, 50, 80, 30, "OK");
	readBtn.labelsize(16);
	readBtn.callback(on_press_read_btn, &pageInput);
	Fl_Box workplaceLabel(480, 30, 120, 30, "Workplace");
	workplaceLabel.labelsize(16);
	workplaceBox = new Fl_Box*[inputSize];
	nowpageBox = new Fl_Box*[inputSize-1];
	int y = 60;

	workplaceBox[0] = new Fl_Box(480, y, 150, 30, "");
	workplaceBox[0]->box(FL_ROUND_DOWN_BOX);
	workplaceBox[0]->labelfont(FL_BOLD);
	y+= 35;
	
	for (int i = 1; i < inputSize; i++) {
		*(workplaceBox + i) = new Fl_Box(480, y, 150, 30, "");
		workplaceBox[i]->box(FL_ROUND_DOWN_BOX);
		workplaceBox[i]->labelfont(FL_BOLD);

		*(nowpageBox + i) = new Fl_Box(400, y, 50, 30, "");
		nowpageBox[i]->box(FL_ROUND_DOWN_BOX);
		nowpageBox[i]->labelfont(FL_BOLD);
		y += 35;
	}
	Page *workplace = cache->workplace;
	string result = "";
	for (int i = 0; i < cache->workplaceSize; i++) {
		stringstream ss;
		ss << workplace[i].name;
		result += ss.str() += " ";
	}
	char *charArrayResult = new char[result.size() + 1];
	charArrayResult[result.size()] = 0;
	memcpy(charArrayResult, result.c_str(), result.size());
	workplaceBox[count++]->label(charArrayResult);

	mainWindow.show();

	return Fl::run();
}