class Page {
	public:
		int name;
		int count;
		Page() {}
		Page(int name) {
			this->name = name;
			this->count = 0;
		}
};

class Cache {
	public:
		int pagesSize;
		int workplaceSize;
		Page pages[10];
		Page workplace[5];

		Cache() {
			pagesSize = 10;
			workplaceSize = 5;

			for (int i = 0; i<pagesSize; i++) pages[i] = Page(i + 1);

			Page unusedPage(-1);
			unusedPage.count = -9999999;
			for (int i = 0; i<workplaceSize; i++)
				workplace[i] = unusedPage;
		}

		void push(int pageName) {
			Page page;
			for (int i = 0; i<pagesSize; i++)
				if (pages[i].name == pageName)
					page = pages[i];

			bool found = false;
			for (int i = 0; i<workplaceSize; i++)
				if (workplace[i].name == pageName) {
					workplace[i].count++;
					found = true;
				}
			

			if (!found) {
				int min = 0;
				for (int i = 1; i<workplaceSize; i++) 
					if (workplace[i].count < workplace[min].count)
						min = i;
				
				for (int i = min; i < workplaceSize; i++)
					workplace[i] = workplace[i + 1];

				workplace[workplaceSize - 1] = page;
	
			}
		}
};