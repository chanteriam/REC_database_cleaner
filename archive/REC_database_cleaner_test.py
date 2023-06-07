from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, get_flashed_messages
import os
import sys
import pandas as pd
import urllib.parse
from cleaner import clean_REC_df
import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set your secret key

def get_fullpath():
    """
    Method for getting the full file path for the application working directory.

    :return (string): Full file path for application working directory.
    """
    if getattr(sys, 'frozen', False):
        # When running as an executable with PyInstaller
        base_path = sys._MEIPASS
    else:
        # When running the script in development mode
        base_path = os.path.abspath(os.path.dirname(__file__))
    return base_path

# @app.route("/", methods=["GET", "POST"])
# def main():

#     # Reset current working directory
#     os.chdir(get_fullpath())

#     if request.method == "POST":
#         if request.files:
#             xlsx_upload = request.files["file"]
#             filename = xlsx_upload.filename

#             inpath = os.path.join("input", filename)
#             outpath = os.path.join("output", filename)
#             fullpath = get_fullpath()

#             xlsx_upload.save(os.path.join(fullpath, inpath))
#             full_outpath = os.path.join(fullpath, outpath)

#             df = clean_REC_df(fullpath, inpath)
#             df.to_excel(full_outpath, index=False)

#             encoded_filepath = urllib.parse.quote_plus(full_outpath)  # Encode the file path
#             print(f"{encoded_filepath}")

#             return redirect(url_for('display_success', filename=filename, encoded_filepath=encoded_filepath))

#     messages = get_flashed_messages()
#     return render_template("index.html", messages=messages)

# @app.route("/input/<filename>/<path:encoded_filepath>")
# def display_success(filename, encoded_filepath):
#     filepath = urllib.parse.unquote_plus(encoded_filepath)  # Decode the file path
#     flash(f"File processed and saved successfully!\nIt was saved here: {filepath}", 'success')
#     return redirect(url_for('main'))


@app.route("/", methods=["GET", "POST"])
def main():
    # Reset current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    if request.method == "POST":
        if request.files:
            xlsx_upload = request.files["file"]
            filename = xlsx_upload.filename

            inpath = os.path.join("input", filename)
            outpath = os.path.join("output", filename)
            fullpath = get_fullpath()

            xlsx_upload.save(os.path.join(fullpath, inpath))
            full_outpath = os.path.join(fullpath, outpath)

            df = clean_REC_df(fullpath, inpath)
            df.to_excel(full_outpath, index=False)

            encoded_filepath = urllib.parse.quote_plus(full_outpath)  # Encode the file path

            return redirect(url_for('download_file', encoded_filepath=encoded_filepath))

    messages = get_flashed_messages()
    return render_template("index.html", messages=messages)

# @app.route("/input/<filename>/<path:encoded_filepath>")
# def display_success(filename, encoded_filepath):
#     message = request.args.get('message')
#     flash(f"File processed successfully: {filename}", message)
#     return redirect(url_for('download_file', encoded_filepath=encoded_filepath))


@app.route("/download/<path:encoded_filepath>")
def download_file(encoded_filepath):
    filepath = urllib.parse.unquote_plus(encoded_filepath)  # Decode the file path
    directory, filename = os.path.split(filepath)

    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)
    app.run(debug=False)
