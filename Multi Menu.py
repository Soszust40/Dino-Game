import sys
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QListWidget, 
    QAbstractItemView, # We need this enum for selection modes
    QVBoxLayout,
    QWidget,
    QLabel,
    QStatusBar
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    """
    Main application window demonstrating a multi-select QListWidget.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Select List Example (PySide6)")
        self.setGeometry(300, 300, 400, 300) # x, y, width, height

        # --- Main Layout and Central Widget ---
        # QMainWindow requires a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Use a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # --- Informational Label (Updated) ---
        info_label = QLabel("Click an item to toggle its selection:")
        info_label.setAlignment(Qt.AlignCenter) # Center the text
        layout.addWidget(info_label)

        # --- Create the QListWidget ---
        self.list_widget = QListWidget()
        
        # Add some items to the list
        self.list_widget.addItems([
            "Python", 
            "JavaScript", 
            "C++", 
            "Rust", 
            "Go", 
            "TypeScript",
            "Java",
            "C#"
        ])

        # --- This is the key line (Updated) ---
        # Set the selection mode to toggle items on click.
        # Other options include:
        # - QAbstractItemView.SingleSelection (Default)
        # - QAbstractItemView.ExtendedSelection (Use Ctrl/Shift)
        # - QAbstractItemView.ContiguousSelection (Only items next to each other)
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        
        # Add the list widget to the layout
        layout.addWidget(self.list_widget)
        
        # --- Status Bar ---
        # Add a status bar to show the current selection
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("No items selected.")

        # --- Connect Signals to Slots ---
        # Connect a signal to a function to update on selection change
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        """
        Slot method that is called whenever the list selection changes.
        """
        # Get a list of the *QListWidgetItem* objects that are selected
        selected_items = self.list_widget.selectedItems()
        
        if not selected_items:
            self.status_bar.showMessage("No items selected.")
            return

        # Get the text from each selected item
        selected_texts = [item.text() for item in selected_items]
        
        # Update the status bar with the selection
        self.status_bar.showMessage(f"Selected: {', '.join(selected_texts)}")
        
        # Optional: Print to console for debugging
        print(f"Selected items: {selected_texts}")


# --- Main execution ---
if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the application's event loop
    sys.exit(app.exec())

