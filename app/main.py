import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pillow import apply_blur, apply_sharpen, apply_edge_enhance, apply_smooth

UPLOAD_FOLDER = os.getcwd() + '/static'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])
INPUT_FILENAME = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bp = Blueprint('photo_editor', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# So preview refreshes with any new change
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@bp.route('/', methods=['GET', 'POST'])
def home():
    global INPUT_FILENAME

    if request.method == 'POST':
        submit_button = request.form.get('submit_button')

        if submit_button == 'upload_image':
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect(request.url)

            if file and allowed_file(file.filename):
                INPUT_FILENAME = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME))
                return redirect(url_for('photo_editor.uploaded'))

        # elif button == 'download_image':
        #     if INPUT_FILENAME:
        #         OUTPUT_FILENAME =
        #         return send_file(os.path.join(app.config['UPLOAD_FOLDER'], OUTPUT_FILENAME), as_attachment=True)
        #     else:
        #         return render_template('home.html')

    return render_template('home.html')


@bp.route('/uploaded', methods=['GET', 'POST'])
def uploaded():

    if request.method == 'POST':
        blur_button = request.form.get('blur_button')
        sharpen_button = request.form.get('sharpen_button')
        edge_button = request.form.get('edge_button')
        smooth_button = request.form.get('smooth_button')

        if blur_button:
            apply_blur(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), blur_button)
        elif sharpen_button:
            apply_sharpen(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), sharpen_button)
        elif edge_button:
            apply_edge_enhance(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), edge_button)
        elif smooth_button:
            apply_smooth(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), smooth_button)

    if INPUT_FILENAME:
        return render_template('home.html', filename=INPUT_FILENAME)
    else:
        return render_template('home.html')


app.register_blueprint(bp, url_prefix='/photo_editor')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
