colors = {
    "background": "#2E2F2F",
    "alt_background": "#262626",
    "foreground": "#3b3b3b",
    "text": "#ffffff",
    "alt_text": "#f1ebe1",
    "green": "#8BA888",
    "green_border": "#435740",
    "highlight": "#cddacc",
    "orange": "#ffb86f",
    "red": "#c83e4d",
    "label": "#8BA888",
    "palette": {
        "Window": "background",
        "WindowText": "foreground",
        "Base": "background",
        "AlternateBase": "foreground",
        "ToolTipBase": "background",
        "ToolTipText": "foreground",
        "Text": "text",
        "Button": "foreground",
        "ButtonText": "background",
        "Highlight": "label",
        "HighlightedText": "background",
    },
}

qss = """
	QMainWindow, QWidget {{
		background-color: {background};
	}}
	QVBoxLayout {{
		padding: 0px;
		margin: 0px;
	}}
	QHBoxLayout {{
		padding: 2px;
		margin: 0px;
	}}
	QMenu {{
		background-color: {background};
		color: {text};
		text-align: center; 
		max-width: 150px;
	}}
	QMenu::item:selected {{
		background-color: {foreground};
		color: {text};
	}}
	QVBoxLayout {{
		padding: 0px;
		margin: 0px;
	}}
	QScrollArea QPushButton {{
		background-color: {background};
		color: {foreground};
		border-radius: 10px;
		border: 1px solid {green};
	}}
	QPushButton {{
		background-color: {foreground};
		color: {background};
		border: none;
		padding: 5px;
		min-width: 80px;
	}}
	QPushButton:hover {{
		background-color: {red};
	}}
	QToolTip {{
		background-color: {background};
		color: {text};
		border: 1px solid {foreground};
		padding: 5px;
	}}
	QLabel {{
		color: {alt_text};
		font-weight: bold;
	}}
	QLineEdit {{
		background-color: {background};
		color: {text};
		border: 1px solid {green};
		text-align: AlignCenter;
		margin-right: 4px;
	}}
	#Container {{
		background: {background};
	}}
	#titleBarLayout #iconLabel {{
		background-color: {green};
		color: {text};
		padding-left: 10px;
	}}
	#titleBarLayout QWidget {{
		background-color: {green};
		color: {text};
		margin: 0px;
		padding: 0px;
		font-weight: bold;
	}}
	#titleBarLayout #closeButton {{
		background-color: {green};
		margin: 0px;
		border: none;
	}}
	#titleBarLayout #closeButton:hover {{
		background-color: {alt_text};
		border: none;
	}}
	#typeWidget {{
		margin: 0px;
		padding: 0px;
	}}
	#SnippetTextArea {{
		border: 1px solid {green_border};
		max-height: 34px;
	}}
	#SnippetTextArea QTextarea {{
		padding: 0px;
		margin: 0px;
	}}
	#contentScrollArea {{
		background-color: {foreground};
		border: 1px solid {alt_background};
		padding: 0px;
		margin: 0px 4px 0px 4px;
	}}
	#contentWidget {{
		background-color: {foreground};
		padding: 0px;
		margin: 0px;
	}}
	#typeButton {{
		background-color: {background};
		color: {text};
		font: bold;
		border: 1px solid {foreground};
		padding: 5px;
		min-width: 80px;
	}}
	#typeButton:hover {{
		font: bold;
		background-color: {alt_text};
		color: {background};
	}}
	#typeButton:focus {{
		background-color: {green};
		color: {background};
		font: bold;
		border: none;
		padding: 5px;
		min-width: 80px;
	}}
	#searchBar {{
		border: 1px solid {highlight};
		color: {text};
		padding-left: 5px;
		margin-left: 4px;
	}}
	#searchButton {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {foreground};
		border-radius: 10px;
	}}
	#searchButton:hover {{
		background-color: {green};
		color: {background};
	}}
	#clearButton {{
		background-color: {background};
		color: {text};
		margin: 0px 4px 0px 0px;
		border-radius: 10px;
	}}
	#clearButton:hover {{
		background-color: {orange};
		color: {background};
	}}
	#createButton {{
		background-color: {orange};
		color: {background};
		margin: 0px 4px 4px 4px;
	}}
	#createButton:hover {{
		background-color: {foreground};
		color: {text};
		font: bold;
	}}
    #copyButton {{
		background-color: {green};
		border: 1px solid {foreground};
        min-width: 8px;
        min-height: 10px;
        border-radius: 10px;
	}}
    #copyButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {green};
		padding: 0px;
		margin: 0px;
	}}
	#copyButton:hover {{
        background-color: {alt_text};
	}}
	#editButton {{
		background-color: {text};
		border: 1px solid {foreground};
        min-width: 15px;
		min-height: 10px;
		border-radius: 8px;
	}}
	#editButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {green};
		padding: 0px;
		margin: 0px;
	}}
	#editButton:hover {{
		background-color: {alt_text};
	}}
	#deleteButton {{
		background-color: {red};
		color: {text};
		border: 1px solid {foreground};
		min-width: 5px;
		max-height: 10px;
		border-radius: 5px;
	}}
	#deleteButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {green};
		padding: 0px;
		margin: 0px;
	}}
	#deleteButton:hover {{
		color: {foreground};
		font: bold;
	}}
	#saveButton {{
		margin-bottom: 4px;
		margin-left: 4px;
		background-color: {green};
	}}
	#closePopupButton {{
		margin-bottom: 4px;
		margin-right: 4px;
		color: {text};
	}}
	#themePicker {{
		color: {text};
		background-color: {foreground};
		border: None;
		text-align: center;
	}}
	QComboBox QAbstractItemView {{
		background-color: {foreground};
		color: {text};
	}}
    #snippetTextArea {{
		border: 1px solid {green_border};
	}}
	"""
