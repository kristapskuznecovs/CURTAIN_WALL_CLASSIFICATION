# CW Classification - Facade Element Analysis System

A comprehensive web-based system for analyzing, classifying, and processing facade elements from architectural data. This software is designed for construction and prefabricated facade manufacturing, providing detailed analysis of building facade elements, opening classifications, and production-ready reports.

## 🏗️ What This Software Does

CW Classification is a specialized tool that:

- **Analyzes facade elements** from building designs and architectural data
- **Classifies openings** (windows, doors, etc.) within facade elements
- **Groups similar elements** for efficient manufacturing and production
- **Generates detailed reports** for engineers and factory production teams
- **Creates visual representations** (SVG drawings) of facade elements
- **Provides statistical analysis** of element types and similarities

## 🎯 Target Users

- **Architects** - Analyzing facade designs and element configurations
- **Engineers** - Processing facade data for manufacturing specifications
- **Manufacturers** - Grouping similar elements for efficient production
- **Construction Companies** - Managing facade element classifications and specifications

## 🏛️ Architecture

The system consists of two main components:

### Backend (Python/Flask)
- **File Processing**: Handles CSV data import and validation
- **Element Analysis**: Processes facade elements, profiles, and openings
- **Classification Engine**: Groups and categorizes similar elements
- **Report Generation**: Creates JSON, CSV, and SVG outputs
- **API Endpoints**: RESTful API for frontend communication

### Frontend (React)
- **Modern Web Interface**: Clean, responsive UI built with React and Bootstrap
- **File Upload**: Drag-and-drop CSV file upload with validation
- **Session Management**: Multi-user support with session tracking
- **Real-time Feedback**: Progress tracking and status updates
- **Download Management**: Easy access to generated reports and files

## 📁 Project Structure

```
cw_classification/
├── cw_backend/                 # Python Flask backend
│   ├── src/cw_backend/
│   │   ├── classes/           # Element representation classes
│   │   ├── read_file/         # CSV processing and file handling
│   │   ├── write_file/        # Report generation and analysis
│   │   ├── session/           # Session management
│   │   └── flask_app.py       # Main Flask application
│   └── requirements.txt       # Python dependencies
├── cw_frontend/               # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Application pages
│   │   └── stores/           # State management (MobX)
│   └── package.json          # Node.js dependencies
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** for the backend
- **Node.js 14+** and **npm** for the frontend
- **CSV files** with facade element data

## 📊 Input Data Format

The system expects CSV files with facade element data containing:

- **Profile information**: Element profiles and cross-sections
- **Coordinates**: 3D coordinates (start/end points)
- **Dimensions**: Length, height, width measurements
- **GUIDs**: Unique identifiers for elements and assemblies
- **Delivery numbers**: Manufacturing identifiers

### Required CSV Columns:
- Profile index
- Length
- Start coordinates (X, Y, Z)
- End coordinates (X, Y, Z)
- Part GUID
- Assembly GUID
- Delivery number

## 📈 Output Reports

The system generates several types of reports:

### 1. **Element Classification Report**
- Groups similar facade elements
- Provides element type descriptions
- Size-based categorization

### 2. **Opening Analysis Report**
- Detailed opening classifications
- Opening dimensions and positions
- Opening type assignments

### 3. **Statistical Reports**
- Element type usage statistics
- Group distribution analysis
- Similarity analysis

### 4. **Visual Outputs**
- SVG drawings of facade elements
- Element plane representations
- Opening visualizations

### 5. **JSON Data**
- Structured element data
- Machine-readable format
- API integration ready

## ⚙️ Configuration

The system can be configured through the `settings.py` file:

```python
settings = {
    "max_tolerance": 5,           # Maximum geometric tolerance
    "min_tolerance": 0.25,        # Minimum geometric tolerance
    "write_jsons": True,          # Generate JSON outputs
    "draw_element": True,         # Generate SVG drawings
    "analyze_json": True,         # Perform analysis
    "assign_opening_type": True,  # Classify openings
    # ... more settings
}
```

## 🔧 API Endpoints

### File Management
- `POST /api/upload/<session>` - Upload CSV files
- `GET /api/download/<folder>/<filename>/<session>` - Download files
- `DELETE /api/delete/<folder>/<filename>/<session>` - Delete files

### Processing
- `GET /api/process/<filename>/<session>` - Process uploaded files
- `GET /getResults/<session>` - Get processing results

### Session Management
- `GET /api/resetSession` - Reset current session

## 🛠️ Key Features

### Element Processing
- **Profile Analysis**: Processes beam elements and cross-sections
- **Plane Generation**: Creates element planes from profiles
- **Opening Detection**: Identifies and classifies openings
- **Geometric Validation**: Ensures data integrity

### Classification Engine
- **Similarity Analysis**: Groups similar elements
- **Type Assignment**: Categorizes opening types
- **Size Grouping**: Groups elements by dimensions
- **Statistical Analysis**: Provides usage statistics

### Error Handling
- **Data Validation**: Validates input data integrity
- **Error Logging**: Comprehensive error tracking
- **Bad Element Handling**: Manages problematic elements
- **User Feedback**: Clear error messages and alerts

## 🎨 User Interface

The web interface provides:

- **Intuitive File Upload**: Drag-and-drop CSV file upload
- **Real-time Progress**: Processing status and progress bars
- **Session Management**: Multi-user support
- **Download Center**: Easy access to all generated files
- **Alert System**: User-friendly notifications and error messages

## 🔒 Session Management

The system includes robust session management:

- **Unique Session IDs**: Each user gets a unique session
- **Concurrent Processing**: Multiple users can work simultaneously
- **Session Validation**: Prevents unauthorized access
- **Automatic Cleanup**: Session reset capabilities

## 📝 Use Cases

### 1. **Architectural Analysis**
- Analyze facade designs for element classification
- Generate detailed element specifications
- Create visual representations of facade elements

### 2. **Manufacturing Planning**
- Group similar elements for efficient production
- Generate manufacturing specifications
- Create production-ready reports

### 3. **Quality Control**
- Validate facade element data
- Identify problematic elements
- Generate error reports and logs

### 4. **Project Management**
- Track element classifications across projects
- Generate project-specific reports
- Manage delivery specifications
