import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from pillow import load_image, dupe_image, get_default_slider, apply_enhancers, apply_hue_shift, get_dominant_colors
from pillow import apply_blur, apply_sharpen, apply_edge_enhance, apply_smooth
from pillow import get_image_size, rotate_image, resize_image, crop_image

UPLOAD_FOLDER = os.getcwd() + '/static'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])
INPUT_FILENAME = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


image, slider = None, None
colors = []
width, height = 0, 0
def refresh_parameters(image_path):
    global image, slider, hue_angle, colors, width, height
    image = load_image(image_path)
    slider = get_default_slider()
    width, height = get_image_size(image)
    colors = get_dominant_colors(image_path)


# So preview refreshes with any new change
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/', methods=['GET', 'POST'])
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
                dupe_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), 'copy')
                refresh_parameters(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME))
                return redirect(url_for('uploaded'))

    return render_template('home.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    global image, slider

    if INPUT_FILENAME:
        if request.method == 'POST':
            # Nav
            original_button = request.form.get('original_button')
            download_button = request.form.get('download_button')
            # Sliders
            enhance_button = request.form.get('enhance_button')
            # Hue
            hue_button = request.form.get('hue_button')
            # Filters
            blur_button = request.form.get('blur_button')
            sharpen_button = request.form.get('sharpen_button')
            edge_button = request.form.get('edge_button')
            smooth_button = request.form.get('smooth_button')
            # Rotate/resize/crop
            rotate_button = request.form.get('rotate_button')
            resize_button = request.form.get('resize_button')
            crop_button = request.form.get('crop_button')

            if original_button:
                dupe_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), 'replace')
            if download_button:
                return send_file(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), as_attachment=True)

            if enhance_button:
                slider = {key: float(request.form.get(key)) for key, value in slider.items()}
                apply_enhancers(image, os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), slider)
            if hue_button:
                hue_angle = float(request.form.get('hue_angle'))
                apply_hue_shift(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), hue_angle)

            if blur_button:
                apply_blur(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), blur_button)
            elif sharpen_button:
                apply_sharpen(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), sharpen_button)
            elif edge_button:
                apply_edge_enhance(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), edge_button)
            elif smooth_button:
                apply_smooth(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), smooth_button)

            if rotate_button:
                angle = int(request.form.get('angle'))
                rotate_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), angle)
            elif resize_button:
                n_width = int(request.form.get('width'))
                n_height = int(request.form.get('height'))
                resize_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), n_width, n_height)
            elif crop_button:
                start_x = int(request.form.get('start_x'))
                start_y = int(request.form.get('start_y'))
                end_x = int(request.form.get('end_x'))
                end_y = int(request.form.get('end_y'))
                crop_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), start_x, start_y, end_x, end_y)

            if any([original_button, hue_button, blur_button, sharpen_button, edge_button, smooth_button, rotate_button, resize_button, crop_button]):
                refresh_parameters(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME))

        return render_template('uploaded.html', slider=slider, colors=colors, width=width, height=height, filename=INPUT_FILENAME)
    else:
        return render_template('uploaded.html', slider=slider)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT'))
