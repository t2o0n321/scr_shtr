import tkinter as tk
import yaml

class MousePositionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Mouse Positions")
        
        # Make window semi-transparent
        self.root.attributes('-alpha', 0.7)
        
        # Set full-screen mode without title bar
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        
        # Create a gray canvas
        self.canvas = tk.Canvas(root, bg='gray', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Bind left mouse click to set position
        self.canvas.bind('<Button-1>', self.set_position)
        
        # Bind Escape key to save positions and exit
        self.root.bind('<Escape>', self.save_and_exit)
        
        # Bind 'r' key to reset all positions to zero
        self.root.bind('r', self.reset_positions)
        
        # Load and store initial data
        self.initial_data = self.load_initial_data()
        self.data = self.initial_data.copy()
        self.markers = []
        self.labels = []

    def load_initial_data(self):
        try:
            with open('conf.yaml', 'r') as f:
                data = yaml.safe_load(f) or {}
                # Extract or set default Position section
                position_data = data.get('Position', {})
                return {
                    'Position': {
                        'book_pos_1_x': position_data.get('book_pos_1_x', 0),
                        'book_pos_1_y': position_data.get('book_pos_1_y', 0),
                        'book_pos_2_x': position_data.get('book_pos_2_x', 0),
                        'book_pos_2_y': position_data.get('book_pos_2_y', 0),
                        'next_page_x': position_data.get('next_page_x', 0),
                        'next_page_y': position_data.get('next_page_y', 0)
                    }
                }
        except FileNotFoundError:
            return {'Position': {'book_pos_1_x': 0, 'book_pos_1_y': 0, 'book_pos_2_x': 0, 'book_pos_2_y': 0, 'next_page_x': 0, 'next_page_y': 0}}

    def set_position(self, event):
        # Get click coordinates
        x, y = event.x, event.y
        
        # If fourth click, reset Position section to zeros
        position_keys = ['book_pos_1_x', 'book_pos_1_y', 'book_pos_2_x', 'book_pos_2_y', 'next_page_x', 'next_page_y']
        if all(self.data['Position'].get(k, 0) != 0 for k in position_keys):
            # Clear canvas markers and labels
            for marker in self.markers:
                self.canvas.delete(marker)
            for label in self.labels:
                self.canvas.delete(label)
            # Reset Position section
            self.data['Position'] = {k: 0 for k in position_keys}
            self.markers = []
            self.labels = []
        
        # Determine which position to set
        if self.data['Position']['book_pos_1_x'] == 0 or self.data['Position']['book_pos_1_y'] == 0:
            self.data['Position']['book_pos_1_x'] = x
            self.data['Position']['book_pos_1_y'] = y
            label_text = "book_pos_1"
        elif self.data['Position']['book_pos_2_x'] == 0 or self.data['Position']['book_pos_2_y'] == 0:
            self.data['Position']['book_pos_2_x'] = x
            self.data['Position']['book_pos_2_y'] = y
            label_text = "book_pos_2"
        elif self.data['Position']['next_page_x'] == 0 or self.data['Position']['next_page_y'] == 0:
            self.data['Position']['next_page_x'] = x
            self.data['Position']['next_page_y'] = y
            label_text = "next_page"
        else:
            return
        
        # Add marker
        marker_size = 5
        marker = self.canvas.create_oval(
            x - marker_size, y - marker_size,
            x + marker_size, y + marker_size,
            fill='red'
        )
        self.markers.append(marker)
        
        # Add label to the right of the click position
        label = self.canvas.create_text(
            x + 70, y,
            text=label_text,
            fill='red',
            font=('Arial', 12, 'bold')
        )
        self.labels.append(label)

    def reset_positions(self, event):
        # Reset all positions to zero
        for marker in self.markers:
            self.canvas.delete(marker)
        for label in self.labels:
            self.canvas.delete(label)
        self.data['Position'] = {
            'book_pos_1_x': 0, 'book_pos_1_y': 0,
            'book_pos_2_x': 0, 'book_pos_2_y': 0,
            'next_page_x': 0, 'next_page_y': 0
        }
        self.markers = []
        self.labels = []

    def save_and_exit(self, event):
        # Load original file to preserve other sections
        try:
            with open('conf.yaml', 'r') as f:
                original_data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            original_data = {}
        
        # Update only the Position section
        original_data['Position'] = self.data['Position']
        
        # Save back to YAML file
        with open('conf.yaml', 'w') as f:
            yaml.dump(original_data, f, default_flow_style=False)
        
        # Exit the application
        self.root.quit()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MousePositionGUI(root)
    root.mainloop()