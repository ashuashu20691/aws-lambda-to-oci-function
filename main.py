from flask import Flask, render_template, request, send_file, redirect, url_for
import zipfile
import os
import io

app = Flask(__name__)

def convert_to_oci(aws_code):
    # Create OCI handler from AWS Lambda handler (simple conversion)
    oci_handler = aws_code.replace("exports.handler = async (event, context)", 
                        "module.exports = async function (context)")
    oci_handler = aws_code.replace("exports.handler = function (event, context)", 
                        "module.exports = async function (context)")
    # Create a temporary directory for the function files
    func_dir = "oci_function"
    os.makedirs(func_dir, exist_ok=True)

    # Write handler.js (OCI function entry point)
    with open(os.path.join(func_dir, "handler.js"), "w") as handler_file:
        handler_file.write(oci_handler)

    # Write func.yaml (OCI Function Configuration)
    func_yaml = """\
schema_version: 20180708
name: oci-function
runtime: nodejs
entrypoint: handler.handler
"""
    with open(os.path.join(func_dir, "func.yaml"), "w") as yaml_file:
        yaml_file.write(func_yaml)

    # Generate Dockerfile
    dockerfile_content = """\
    FROM fnproject/node:latest
    WORKDIR /function
    ADD . /function/
    RUN npm install || :
    CMD ["node", "func.js"]
    """
    with open(os.path.join(func_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        zipf.write(os.path.join(func_dir, "handler.js"), "handler.js")
        zipf.write(os.path.join(func_dir, "func.yaml"), "func.yaml")
        zipf.write(os.path.join(func_dir, "Dockerfile"), "Dockerfile")
    
    zip_buffer.seek(0)  # Rewind the buffer to the beginning

    # Cleanup temporary files
    os.remove(os.path.join(func_dir, "handler.js"))
    os.remove(os.path.join(func_dir, "func.yaml"))
    os.remove(os.path.join(func_dir, "Dockerfile"))
    os.rmdir(func_dir)

    return zip_buffer

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        aws_code = request.form.get("aws_lambda_code").strip()
        if not aws_code:
            return render_template("index.html", error="Please paste AWS Lambda code!")

        zip_buffer = convert_to_oci(aws_code)
        return send_file(zip_buffer, as_attachment=True, download_name="oci_function.zip", mimetype="application/zip")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

