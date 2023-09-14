from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash,
    send_file,
    get_flashed_messages,
)
import os
import sys
import pandas as pd
import urllib.parse
from scripts.cleaner import main
import webbrowser
from datetime import date

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Set your secret key


def get_fullpath():
    """
    Method for getting the full file path for the application working directory.

    :return (string): Full file path for application working directory.
    """
    if getattr(sys, "frozen", False):
        # When running as an executable with PyInstaller
        base_path = sys._MEIPASS
    else:
        # When running the script in development mode
        base_path = os.path.abspath(os.path.dirname(__file__))
    return base_path


@app.route("/", methods=["GET", "POST"])
def upload_data():
    # Reset current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    if request.method == "POST":
        if request.files:
            source = request.form["source"]

            upload = request.files["file"]
            filename = upload.filename

            inpath = os.path.join("input", filename)
            outpath = os.path.join("output", filename)
            fullpath = get_fullpath()

            upload.save(os.path.join(fullpath, inpath))
            full_outpath = os.path.join(fullpath, outpath)

            df = main(fullpath, inpath, source)
            print("RENDERED")

            if ".xlsx" in full_outpath:
                full_outpath = full_outpath.split(".xlsx")[0] + ".csv"
            df.to_csv(full_outpath, index=False)

            encoded_filepath = urllib.parse.quote_plus(
                full_outpath
            )  # Encode the file path

            return redirect(url_for("download_file", encoded_filepath=encoded_filepath))

    messages = get_flashed_messages()
    return render_template("index.html", messages=messages)


@app.route("/download/<path:encoded_filepath>")
def download_file(encoded_filepath):
    filepath = urllib.parse.unquote_plus(encoded_filepath)  # Decode the file path
    directory, filename = os.path.split(filepath)

    today = date.today()

    cleaned_filename = (
        os.path.splitext(filename)[0] + f"_cleaned_{today.strftime('%m%d%Y')}.csv"
    )
    return send_file(filepath, as_attachment=True, download_name=cleaned_filename)


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)
    app.run(debug=False)
