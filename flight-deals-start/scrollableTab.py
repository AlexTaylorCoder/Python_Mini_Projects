from scrollableFrame import ScrollableFrame

class ScrollableTab(ScrollableFrame):
    def __init__(self, tabView,name, *args, **kwargs):
        super().__init__(tabView,name *args, **kwargs)
        self.name = self.tabView.add(name)
        self.sFrame = ScrollableFrame(self.name)

