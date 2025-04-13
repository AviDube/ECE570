import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                            QSlider, QGroupBox, QComboBox, QFrame, QSplitter,
                            QProgressBar, QMessageBox, QToolTip, QStyle)
from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint

class ModernFrame(QFrame):
    """A custom frame with rounded corners and shadow effect"""
    def __init__(self, parent=None):
        super(ModernFrame, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            ModernFrame {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)

class StyledButton(QPushButton):
    """A custom styled button"""
    def __init__(self, text, parent=None, primary=True):
        super(StyledButton, self).__init__(text, parent)
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4a86e8;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3a76d8;
                }
                QPushButton:pressed {
                    background-color: #2a66c8;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #888888;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QPushButton:disabled {
                    background-color: #f8f8f8;
                    color: #bbbbbb;
                    border: 1px solid #dddddd;
                }
            """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class EnhancedCartoonUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Cartoonizer")
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 20px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 6px;
                min-width: 6em;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #4a86e8;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #cccccc;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background-color: #dddddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #4a86e8;
                border: none;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::add-page:horizontal {
                background-color: #dddddd;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background-color: #4a86e8;
                border-radius: 4px;
            }
            QToolTip {
                background-color: #2a2a2a;
                color: white;
                border: none;
                font-size: 13px;
                padding: 5px;
            }
        """)
        
        self.original_image = None
        self.cartoon_image = None
        
        self.processing = False
        
        self.init_ui()
        
        QTimer.singleShot(500, self.show_welcome_message)
    
    def show_welcome_message(self):
        welcome_box = QMessageBox(self)
        welcome_box.setWindowTitle("Welcome to Image Cartoonizer")
        welcome_box.setIcon(QMessageBox.Information)
        welcome_box.setText("<h3>Welcome to Image Cartoonizer!</h3>")
        welcome_box.setInformativeText(
            "This app lets you transform your photos into cartoon style images. "
            "To get started:<br><br>"
            "1. Click <b>Load Image</b> to select a photo<br>"
            "2. Choose a cartoon style<br>"
            "3. Adjust the parameters to your liking<br>"
            "4. Click <b>Cartoonize!</b><br><br>"
            "Have fun creating cartoon versions of your photos!"
        )
        welcome_box.setStandardButtons(QMessageBox.Ok)
        welcome_box.exec_()
        
    def init_ui(self):
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        title_label = QLabel("Image Cartoonizer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4a86e8;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)
        
        desc_label = QLabel("Transform your photos into beautiful cartoon-style artwork")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("font-size: 14px; color: #666666; margin-bottom: 15px;")
        main_layout.addWidget(desc_label)
        
        content_splitter = QSplitter(Qt.Horizontal)
        
        images_frame = ModernFrame()
        images_layout = QVBoxLayout(images_frame)
        images_layout.setContentsMargins(15, 15, 15, 15)
        
        images_splitter = QSplitter(Qt.Horizontal)
        
        original_container = QWidget()
        original_layout = QVBoxLayout(original_container)
        original_layout.setContentsMargins(0, 0, 0, 0)
        
        self.original_label = QLabel("Original Image")
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        
        self.original_display = QLabel()
        self.original_display.setMinimumSize(300, 300)
        self.original_display.setAlignment(Qt.AlignCenter)
        self.original_display.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #cccccc;
            border-radius: 5px;
            color: #888888;
        """)
        self.original_display.setText("No image loaded")
        
        original_layout.addWidget(self.original_label)
        original_layout.addWidget(self.original_display, 1)
        
        cartoon_container = QWidget()
        cartoon_layout = QVBoxLayout(cartoon_container)
        cartoon_layout.setContentsMargins(0, 0, 0, 0)
        
        self.cartoon_label = QLabel("Cartoonized Image")
        self.cartoon_label.setAlignment(Qt.AlignCenter)
        self.cartoon_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        
        self.cartoon_display = QLabel()
        self.cartoon_display.setMinimumSize(300, 300)
        self.cartoon_display.setAlignment(Qt.AlignCenter)
        self.cartoon_display.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #cccccc;
            border-radius: 5px;
            color: #888888;
        """)
        self.cartoon_display.setText("Cartoonized image will appear here")
        
        cartoon_layout.addWidget(self.cartoon_label)
        cartoon_layout.addWidget(self.cartoon_display, 1)
        
        images_splitter.addWidget(original_container)
        images_splitter.addWidget(cartoon_container)
        images_splitter.setSizes([int(self.width()/2), int(self.width()/2)])
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #f0f0f0;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #4a86e8;
                border-radius: 3px;
            }
        """)
        self.progress_bar.hide()
        
        images_layout.addWidget(images_splitter)
        images_layout.addWidget(self.progress_bar)
        
        controls_frame = ModernFrame()
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(20, 20, 20, 20)
        controls_layout.setSpacing(15)
        
        file_group = QGroupBox("1. Select Image")
        file_layout = QVBoxLayout(file_group)
        file_layout.setContentsMargins(15, 25, 15, 15)
        file_layout.setSpacing(10)
        
        self.load_button = StyledButton("Load Image", primary=True)
        self.load_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.load_button.setIconSize(QSize(20, 20))
        self.load_button.setToolTip("Click to select an image from your computer")
        self.load_button.clicked.connect(self.load_image)
        file_layout.addWidget(self.load_button)
        
        style_group = QGroupBox("2. Choose Style")
        style_layout = QVBoxLayout(style_group)
        style_layout.setContentsMargins(15, 25, 15, 15)
        style_layout.setSpacing(10)
        
        style_label = QLabel("Cartoon Style:")
        style_label.setToolTip("Select the type of cartoon effect to apply")
        
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Anime", "Comic Book", "Pixar-like", "Watercolor"])
        self.style_combo.setToolTip("Different cartoon styles will produce different effects")
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combo)
        
        params_group = QGroupBox("3. Adjust Parameters")
        params_layout = QVBoxLayout(params_group)
        params_layout.setContentsMargins(15, 25, 15, 15)
        params_layout.setSpacing(15)
        
        
        detail_layout = QVBoxLayout()
        detail_label = QLabel("Detail Level:")
        detail_value = QLabel("50%")
        detail_value.setAlignment(Qt.AlignRight)
        detail_header = QHBoxLayout()
        detail_header.addWidget(detail_label)
        detail_header.addWidget(detail_value)
        
        self.detail_slider = QSlider(Qt.Horizontal)
        self.detail_slider.setMinimum(0)
        self.detail_slider.setMaximum(100)
        self.detail_slider.setValue(50)
        self.detail_slider.setTickPosition(QSlider.TicksBelow)
        self.detail_slider.setTickInterval(10)
        self.detail_slider.setToolTip("Adjust how detailed the cartoon effect will be")
        self.detail_slider.valueChanged.connect(lambda v: detail_value.setText(f"{v}%"))
        
        detail_layout.addLayout(detail_header)
        detail_layout.addWidget(self.detail_slider)
        params_layout.addLayout(detail_layout)
        
        color_layout = QVBoxLayout()
        color_label = QLabel("Color Intensity:")
        color_value = QLabel("50%")
        color_value.setAlignment(Qt.AlignRight)
        color_header = QHBoxLayout()
        color_header.addWidget(color_label)
        color_header.addWidget(color_value)
        
        self.color_slider = QSlider(Qt.Horizontal)
        self.color_slider.setMinimum(0)
        self.color_slider.setMaximum(100)
        self.color_slider.setValue(50)
        self.color_slider.setTickPosition(QSlider.TicksBelow)
        self.color_slider.setTickInterval(10)
        self.color_slider.setToolTip("Adjust the vibrancy of colors in the cartoon")
        self.color_slider.valueChanged.connect(lambda v: color_value.setText(f"{v}%"))
        
        color_layout.addLayout(color_header)
        color_layout.addWidget(self.color_slider)
        params_layout.addLayout(color_layout)
        
        edge_layout = QVBoxLayout()
        edge_label = QLabel("Edge Strength:")
        edge_value = QLabel("50%")
        edge_value.setAlignment(Qt.AlignRight)
        edge_header = QHBoxLayout()
        edge_header.addWidget(edge_label)
        edge_header.addWidget(edge_value)
        
        self.edge_slider = QSlider(Qt.Horizontal)
        self.edge_slider.setMinimum(0)
        self.edge_slider.setMaximum(100)
        self.edge_slider.setValue(50)
        self.edge_slider.setTickPosition(QSlider.TicksBelow)
        self.edge_slider.setTickInterval(10)
        self.edge_slider.setToolTip("Adjust the strength of outlines in the cartoon")
        self.edge_slider.valueChanged.connect(lambda v: edge_value.setText(f"{v}%"))
        
        edge_layout.addLayout(edge_header)
        edge_layout.addWidget(self.edge_slider)
        params_layout.addLayout(edge_layout)
        
        action_group = QGroupBox("4. Process Image")
        action_layout = QVBoxLayout(action_group)
        action_layout.setContentsMargins(15, 25, 15, 15)
        action_layout.setSpacing(10)
        
        self.apply_button = StyledButton("Cartoonize!", primary=True)
        self.apply_button.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.apply_button.setIconSize(QSize(20, 20))
        self.apply_button.setToolTip("Apply the cartoon effect to your image")
        self.apply_button.clicked.connect(self.apply_cartoon)
        self.apply_button.setEnabled(False)
        
        self.save_button = StyledButton("Save Image", primary=False)
        self.save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_button.setIconSize(QSize(20, 20))
        self.save_button.setToolTip("Save your cartoonized image to your computer")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        
        action_layout.addWidget(self.apply_button)
        action_layout.addWidget(self.save_button)
        
        controls_layout.addWidget(file_group)
        controls_layout.addWidget(style_group)
        controls_layout.addWidget(params_group)
        controls_layout.addWidget(action_group)
        controls_layout.addStretch()
        
        content_splitter.addWidget(images_frame)
        content_splitter.addWidget(controls_frame)
        
        content_splitter.setSizes([int(self.width()*0.65), int(self.width()*0.35)])
        
        main_layout.addWidget(content_splitter, 1)
        
        status_bar = QLabel("Ready to cartoonize your images!")
        status_bar.setStyleSheet("color: #666666; font-size: 12px;")
        status_bar.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(status_bar)
        
        self.setCentralWidget(main_container)
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select an Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        
        if file_path:
            try:
                self.original_image = cv2.imread(file_path)
                if self.original_image is not None:
                    self.display_image(self.original_image, self.original_display)
                    self.apply_button.setEnabled(True)
                    
                    QToolTip.showText(
                        self.apply_button.mapToGlobal(QPoint(0, 0)),
                        "Your image is loaded! Click 'Cartoonize!' to transform it.",
                        self.apply_button,
                        self.apply_button.rect(),
                        2000
                    )
                else:
                    self.show_error("Could not load the image. Please try another file.")
            except Exception as e:
                self.show_error(f"Error loading image: {str(e)}")
    
    def apply_cartoon(self):
        if self.original_image is not None and not self.processing:
            self.processing = True
            self.progress_bar.show()
            self.apply_button.setEnabled(False)
            self.load_button.setEnabled(False)
            self.apply_button.setText("Processing...")
            
            self.animate_progress()
            
            # How the slider values would be stored into variables
            # style = self.style_combo.currentText()
            # detail_level = self.detail_slider.value()
            # color_intensity = self.color_slider.value()
            # edge_strength = self.edge_slider.value()
            
            QTimer.singleShot(1500, lambda: self.process_complete(self.original_image))
    
    def process_complete(self, processed_image):
        # Place holder for now while I work on figuring out the cartoonization logic
        self.cartoon_image = processed_image.copy()
        
        self.display_image(self.cartoon_image, self.cartoon_display)
        
        self.progress_bar.setValue(100)
        QTimer.singleShot(300, lambda: self.progress_bar.hide())
        self.save_button.setEnabled(True)
        self.apply_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.apply_button.setText("Cartoonize!")
        self.processing = False
        
        QMessageBox.information(
            self,
            "Success!",
            "Your image has been cartoonized! You can now save it or try different settings."
        )
    
    def animate_progress(self):
        """Animate the progress bar to simulate processing"""
        current_value = self.progress_bar.value()
        if current_value < 95 and self.processing:
            increment = max(1, int((95 - current_value) / 10))
            new_value = min(95, current_value + increment)
            self.progress_bar.setValue(new_value)
            QTimer.singleShot(100, self.animate_progress)
    
    def save_image(self):
        if self.cartoon_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Cartoonized Image", 
                "cartoonized_image.png", 
                "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
            )
            
            if file_path:
                try:
                    cv2.imwrite(file_path, self.cartoon_image)
                    QMessageBox.information(
                        self,
                        "Image Saved",
                        f"Your cartoonized image has been saved successfully to:\n{file_path}"
                    )
                except Exception as e:
                    self.show_error(f"Error saving image: {str(e)}")
    
    def show_error(self, message):
        """Display an error message"""
        QMessageBox.critical(self, "Error", message)
    
    def display_image(self, img, display_label):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        h, w, c = img_rgb.shape
        display_w = display_label.width()
        display_h = display_label.height()
        
        aspect_ratio = w / h
        
        if w > h:
            new_w = min(display_w, w)
            new_h = int(new_w / aspect_ratio)
            if new_h > display_h:
                new_h = display_h
                new_w = int(new_h * aspect_ratio)
        else:
            new_h = min(display_h, h)
            new_w = int(new_h * aspect_ratio)
            if new_w > display_w:
                new_w = display_w
                new_h = int(new_w / aspect_ratio)
        
        img_scaled = cv2.resize(img_rgb, (new_w, new_h))
        
        height, width, channel = img_scaled.shape
        bytes_per_line = 3 * width
        q_img = QImage(img_scaled.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        
        display_label.setText("")
        display_label.setPixmap(pixmap)
        display_label.setAlignment(Qt.AlignCenter)
        
        display_label.setStyleSheet("""
            background-color: #f8f8f8;
            border: 1px solid #dddddd;
            border-radius: 5px;
        """)


app = QApplication(sys.argv)
window = EnhancedCartoonUI()
window.show()
sys.exit(app.exec_())