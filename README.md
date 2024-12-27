# AWS Lambda to OCI Function Converter

This project provides a web interface for converting AWS Lambda functions (written in Node.js) into OCI Function-compatible format.

---

## Features
- Accept AWS Lambda Node.js code as input.
- Convert Lambda function to OCI Function format.
- Provide clear steps for deploying the generated OCI Function using the Fn Project CLI.

---

## Prerequisites

### For Deployment
1. Ensure [OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) is installed and configured.
2. Install the [Fn Project CLI](https://fnproject.io/).
3. Set up an OCI Functions application in the target compartment.
4. A modern web browser for running the interface.

---

## How to Use
1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```
2. Run the application:
    ```bash
    flask run
    ```
3. Open a web browser and navigate to `http://127.0.0.1:5000`.
4. Paste your AWS Lambda Node.js code in the provided input field and click "Convert to OCI Function."
5. Download the generated OCI Function zip file.

---

## Deployment Steps Using Fn Project CLI
1. Open a terminal and navigate to the directory containing the downloaded ZIP file.
2. Extract the ZIP file contents:
    ```bash
    unzip <filename>.zip
    ```
3. Initialize the function:
    ```bash
    fn init --runtime node oci-function
    ```
4. Deploy the function to OCI Functions:
    ```bash
    fn -v deploy --app <app-name>
    ```
    - Replace `<app-name>` with the name of the target OCI Functions application.

5. Validate and test the function deployment using the OCI Console or CLI.

---

## Project Structure
- `templates/index.html`: Contains the web interface for the converter.
- `app.py`: Main Flask application file.
- `static/`: Directory for CSS or JS assets (if any).

---

---

## Contributing
Feel free to open issues or submit pull requests for improvements and bug fixes.

---

## Contact
For further inquiries, please contact [Ashu Kumar/ashuashu20691@gmail.com].